import json

import awswrangler as wr
import boto3
import pandas as pd
import psycopg2
import requests
from psycopg2.extras import execute_batch
from sqlalchemy import create_engine


def get_airbyte_access_token(client_id: str, client_secret: str) -> str:
    url = "https://api.airbyte.com/v1/applications/token"
    headers = {"accept": "application/json", "content-type": "application/json"}

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant-type": "client_credentials",
    }

    response = requests.post(url, headers=headers, json=payload)
    return json.loads(response.text)["access_token"]


def run_airbyte_sync(access_token: str, conn_id: str) -> str:
    url = "https://api.airbyte.com/v1/jobs"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
    }

    payload = {"connectionId": conn_id, "jobType": "sync"}

    response = requests.post(url, headers=headers, json=payload)
    return json.loads(response.text)["jobId"]


def get_job_status(job_id, access_token):
    url = f"https://api.airbyte.com/v1/jobs/{job_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)

    return json.loads(response.text)


def get_data_from_s3(session: boto3.Session, s3_path: str) -> pd.DataFrame:
    """
    Read transaction data from an S3 path.

    :param session: boto3 session
    :param s3_path: path to file in s3
    :return: pandas dataframe created from the specified S3 path.
    """

    return wr.s3.read_csv(s3_path, boto3_session=session)


def aws_session(aws_access_key_id: str, aws_secret_access_key: str) -> boto3.Session:
    """
    Create a boto3 session.

    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :return: boto3 session
    """

    # recieved from env variables
    return boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


def establish_connection(host, port, db, user, password):
    """
     Establish a connection to a PostgreSQL database.

    :param host: PostgreSQL host address
    :param port:  PostgreSQL port number. Default is 5432.
    :param db:  PostgreSQL database name.
    :param user:  PostgreSQL database user.
    :param password: PostgreSQL database password.
    :return: Cursor for executing SQL queries.
    """

    conn = psycopg2.connect(
        host=host, database=db, user=user, password=password, port=port
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    print(f"connected to {db} database")

    return cur


def write_data_to_db(database_obj: dict, query: str, data: list[dict]):
    """
    Write data to a PostgreSQL database.

    :param database_obj: Dictionary containing database connection details (host, user, port, db, password).
    :param query: SQL query for inserting data.
    :param data: List of dictionaries representing the data to be inserted.
    :return:
    """
    cur = establish_connection(
        host=database_obj["host"],
        user=database_obj["user"],
        port=database_obj["port"],
        db=database_obj["db"],
        password=database_obj["password"],
    )
    execute_batch(cur, query, data, page_size=1000)
    print("batch insert complete")
