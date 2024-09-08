"""
This DAG is designed to extract engagement metrics from a specified file path and load them into a database.
It includes tasks to check for file availability, read the file, transform the data, and load the data into a database.
"""

import datetime as dt
import json
import os
import time

import boto3
import numpy as np
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task, task_group
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import get_current_context
from airflow.providers.http.sensors.http import HttpSensor
from pendulum import datetime, duration
from sqlalchemy import create_engine

from include.helpers.slack import send_notification as slack_notify
from include.helpers.utils import (
    aws_session,
    get_airbyte_access_token,
    get_data_from_s3,
    get_job_status,
    run_airbyte_sync,
    write_data_to_db,
)
from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig, LoadMode
from include.others.sql import ClientEngagementMetrics
from include.others.transformations import (
    clean_service,
    clean_sub_service,
    format_revenue,
)



# for demo purpose we use env, a secret backend should be used here
ENV = {
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("PORT"),
    "db": os.getenv("DATABASE"),
    "user": os.getenv("POSTGRES_DB_USER"),
    "password": os.getenv("PASSWORD"),
    "airbyte_sync_connection_id": os.getenv("AIRBYTE_CONNECTION_ID"),
    "airbyte_client_id": os.getenv("AIRBYTE_CLIENT_ID"),
    "airbyte_client_secret": os.getenv("AIRBYTE_CLIENT_SECRET"),
}

DBT_ENV = {
    "SNOWFLAKE_USER": os.getenv("SNOWFLAKE_USER") ,
    "SNOWFLAKE_PASSWORD": os.getenv("SNOWFLAKE_PASSWORD"),
    "SNOWFLAKE_ACCOUNT": os.getenv("SNOWFLAKE_ACCOUNT"),
    "SNOWFLAKE_ROLE_NAME": os.getenv("SNOWFLAKE_ROLE_NAME"),
    "SNOWFLAKE_DATABASE": os.getenv("SNOWFLAKE_DATABASE"),
    "SNOWFLAKE_WAREWHOUSE": os.getenv("SNOWFLAKE_WAREWHOUSE"),
    "SNOWFLAKE_SCHEMA": os.getenv("SNOWFLAKE_SCHEMA"),
    "ENVIRONMENT": "dev"
}

run_ts = "{{ execution_date.strftime('%Y-%m-%d') }}"

PROJECT_DIR = os.getcwd()
BUCKET = "superside-mide"
BUCKET_KEY = "raw/client-engagement/engagement-{}.csv"

word_numeric_map = {
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000,
}


default_args = {
    "on_failure_callback": slack_notify,
    "owner": "mide",
    "retries": 1,
    "retry_delay": duration(minutes=1),
}

dag = DAG(
    dag_id="extract_engagement_metrics",
    start_date=datetime(2024, 9, 3),
    schedule=None,  # self trigger
    max_active_runs=1,
    catchup=False,
    default_args=default_args,
)
dag.doc_md = __doc__


@task(dag=dag)
def check_file_availability(file_date: str) -> bool:
    """
    Check if a file exists at the specified path.

    Args:
        run_date (str): the date of the run

    """
    print(f"Checking file availability for {BUCKET_KEY}")
    session = aws_session(ENV["aws_access_key_id"], ENV["aws_secret_access_key"])

    s3 = session.resource("s3")

    context = get_current_context()
    ti = context["ti"]

    try:
        s3.Object(BUCKET, BUCKET_KEY.format(file_date)).get()

    except Exception as e:
        raise e


@task(dag=dag, trigger_rule="none_failed")
def load_data_to_postgres(file_date, **context):
    session = aws_session(ENV["aws_access_key_id"], ENV["aws_secret_access_key"])
    df = get_data_from_s3(session, f"s3://{BUCKET}/{BUCKET_KEY.format(file_date)}")

    df = clean_service(df, "Service")
    df = clean_service(df, "Service Type")
    df = clean_sub_service(df, "Sub-Service")
    df = clean_sub_service(df, "Detailed Sub-Service")

    df["Employee Count"].replace(np.nan, "", inplace=True)
    df["Customer Name"].replace(np.nan, "", inplace=True)
    df["Engagement Date"].replace(np.nan, "", inplace=True)

    df["Engagement Type"] = df["Engagement Type"].str.replace(
        r"(?i)^one.*|.*ime$", "One-time", regex=True
    )
    df["Engagement Type"] = df["Engagement Type"].str.replace(
        r"(?i)^rec.*|.*ing$", "Recurring", regex=True
    )
    df["Engagement Type"] = df["Engagement Type"].str.replace(
        r"(?i)^n.*|.*w$", "New", regex=True
    )

    df["Engagement Date"] = df["Engagement Date"].str.replace(".", "-")
    df["Engagement Date"] = pd.to_datetime(
        df["Engagement Date"], format="mixed"
    ).dt.date
    df["Engagement Date"] = df["Engagement Date"].astype(str)
    df["Engagement Date"].replace("NaT", None, inplace=True)

    df.loc[df["Employee Count"].str.isalpha(), "Employee Count"] = (
        df["Employee Count"].map(word_numeric_map).astype("Int64")
    )

    df["Employee Count"].replace("", None, inplace=True)
    df["Employee Count"] = df["Employee Count"].astype("float").astype("Int64")

    df["Customer ID"] = df["Customer ID"].astype("Int64")

    df = format_revenue(df, "Revenue")
    df = format_revenue(df, "Revenue USD")
    df = format_revenue(df, "Client Revenue")
    df["Load Date"] = context["ts"]
    df["Load Date"] = pd.to_datetime(df["Load Date"])
    df["Load Date"] = df["Load Date"].astype(str)
    df["Engagement Date"].replace("NaT", None, inplace=True)
    df["ID"] = (
        df["Project ID"].astype(str)
        + "+"
        + df["EngagementID"].astype(str)
        + "+"
        + str(file_date)
    )
    df.drop_duplicates(subset=["ID"], inplace=True)
    data = json.loads(df.to_json(orient="records"))

    write_data_to_db(ENV, ClientEngagementMetrics, data)


@task(dag=dag, trigger_rule="none_failed")
def sync_postgres_to_snowflake(**context):
    access_token = get_airbyte_access_token(
        ENV["airbyte_client_id"], ENV["airbyte_client_secret"]
    )
    job_id = run_airbyte_sync(access_token, ENV["airbyte_sync_connection_id"])
    ti = context["ti"]
    ti.xcom_push("job_id", job_id)

    return job_id


@task(dag=dag, trigger_rule="none_failed")
def wait_for_sync_completion(**context):
    ti = context["ti"]
    job_id = ti.xcom_pull(key="job_id", task_ids="sync_postgres_to_snowflake")
    access_token = get_airbyte_access_token(
        ENV["airbyte_client_id"], ENV["airbyte_client_secret"]
    )
    start_time = time.time()
    while True:
        status = get_job_status(job_id, access_token)
        if status["status"] == "succeeded":
            return status
        elif status["status"] != "succeeded" and status["status"] != "running":
            raise Exception(status)
        elif time.time() - start_time > 1800:
            raise Exception("Timed out")
        else:
            time.sleep(5)


dbt = DbtTaskGroup(
        dag=dag,
        group_id="transform_engagement_metrics",
        project_config=ProjectConfig(
            dbt_project_path=os.path.join(PROJECT_DIR, "dbt"),
            env_vars=DBT_ENV,
        ),

        execution_config=ExecutionConfig(
            dbt_executable_path="dbt",
        ),
        profile_config=ProfileConfig(
            profiles_yml_filepath=os.path.join(PROJECT_DIR, "dbt/profiles.yml"),
            profile_name="superside",
            target_name=DBT_ENV["ENVIRONMENT"],

        ),
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS
        ),
        operator_args={
            "append_env": True,
            "install_deps": True,
        },

    )
check_file_availability = check_file_availability(run_ts)
load_data_to_postgres = load_data_to_postgres(run_ts)
sync_postgres_to_snowflake = sync_postgres_to_snowflake()
wait_for_completion = wait_for_sync_completion()

(
    check_file_availability
    >> load_data_to_postgres
    >> sync_postgres_to_snowflake
    >> wait_for_completion
    >> dbt
)
