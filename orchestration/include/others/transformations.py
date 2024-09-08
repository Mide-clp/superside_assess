import numpy as np
import pandas as pd


def clean_service(service_df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Cleans the service column by replacing the service names with their corresponding service types.

    Args:
        service_df (pd.DataFrame): The DataFrame containing the necessary data.
        column_name (str): The name of the column to be cleaned.
    :param service_df:
    :param column_name:
    :return: df: The cleaned DataFrame.
    """
    service_df[column_name] = service_df[column_name].str.replace(
        r"(?i)^dev.*|.*ent$", "Development", regex=True
    )
    service_df[column_name] = service_df[column_name].str.replace(
        r"(?i)^des.*|.*ign$", "Design", regex=True
    )
    service_df[column_name] = service_df[column_name].str.replace(
        r"(?i)^con.*|.*ing$", "Strategy", regex=True
    )
    service_df[column_name] = service_df[column_name].str.replace(
        r"(?i)^sup.*|.*ort$", "Support", regex=True
    )

    return service_df


def clean_sub_service(sub_service_df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Cleans the sub-service column by replacing the sub-service names with their corresponding sub-service types.

    Args:
        sub_service_df (pd.DataFrame): The DataFrame containing the necessary data.
        column_name (str): The name of the column to be cleaned.
    :param sub_service_df:
    :param column_name:
    :return: df: The cleaned DataFrame.
    """
    sub_service_df[column_name] = sub_service_df[column_name].str.replace(
        r"(?i)^bac.*|.*kend$", "Backend", regex=True
    )
    sub_service_df[column_name] = sub_service_df[column_name].str.replace(
        r"(?i)^fro.*|.*tend$", "Frontend", regex=True
    )
    sub_service_df[column_name] = sub_service_df[column_name].str.replace(
        r"(?i)^cus.*|.*ice$", "Customer Service", regex=True
    )
    sub_service_df[column_name] = sub_service_df[column_name].str.replace(
        r"(?i)^str.*|.*egy$", "Strategy", regex=True
    )
    sub_service_df[column_name] = sub_service_df[column_name].str.replace(
        r"(?i)^u.*|.*i$", "UX/UI", regex=True
    )

    return sub_service_df


def format_revenue(revenue_df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Cleans the revenue column by replacing the currency symbol and thousand indicator with their corresponding values.

    Args:
        revenue_df (pd.DataFrame): The DataFrame containing the necessary data.
        column_name (str): The name of the column to be formatted.
    :param revenue_df: The DataFrame containing the necessary data.
    :param column_name: The name of the column to be cleaned.
    :return: df: The cleaned DataFrame.
    """
    revenue_df[column_name].replace(np.nan, "", inplace=True)
    if "usd" not in column_name.lower():
        revenue_df.loc[
            (revenue_df[column_name] != "")
            & (revenue_df[column_name].str.contains(r"\$", regex=True)),
            f"{column_name} Currency",
        ] = "$"

        revenue_df[f"{column_name} Currency"].replace(np.nan, "", inplace=True)

    revenue_df.loc[
        (revenue_df[column_name] != "") & (revenue_df[column_name].str.contains("k")),
        f"{column_name} IsThousand",
    ] = True
    revenue_df[column_name] = revenue_df[column_name].replace(r"\$", "", regex=True)
    revenue_df[column_name] = revenue_df[column_name].replace(r"k", "", regex=True)
    revenue_df[column_name] = revenue_df[column_name].replace(
        r"(?i)\s+USD$", "", regex=True
    )
    revenue_df[column_name] = revenue_df[column_name].replace(np.nan, None)
    revenue_df[f"{column_name} IsThousand"] = revenue_df[
        f"{column_name} IsThousand"
    ].replace(np.nan, None)
    revenue_df[column_name] = revenue_df.apply(
        lambda row: (
            float(row[column_name]) * 1000
            if row[f"{column_name} IsThousand"]
            else row[column_name]
        ),
        axis=1,
    )

    revenue_df.drop(columns=[f"{column_name} IsThousand"], inplace=True)

    revenue_df[column_name].replace("", None, inplace=True)
    revenue_df[column_name] = revenue_df[column_name].astype("Float64")

    return revenue_df
