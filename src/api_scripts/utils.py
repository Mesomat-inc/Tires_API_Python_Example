from datetime import datetime
import os
import pandas as pd


def is_iso_8601(timestamp: str) -> bool:
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False


def format_headers():
    return {"token": os.getenv("ACCESS_TOKEN")}


def convert_json_to_dataframe(json_data: dict) -> pd.DataFrame:
    """
    Convert a JSON object to a pandas DataFrame
    Args:
        json_data (dict): the JSON object to convert
    """
    return pd.DataFrame(json_data)
