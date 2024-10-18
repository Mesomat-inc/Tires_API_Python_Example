from datetime import datetime
import os
import pandas as pd
from dotenv import set_key

def is_iso_8601(timestamp: str) -> bool:
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False

def update_dotenv_key(key, value):
    set_key(".env", key, value)
    print(f"{key} was updated")

def convert_sensor_data_to_dataframe(json_data: dict) -> pd.DataFrame:
    """
    Convert a JSON object containing sensor data to a pandas DataFrame
    Args:
        json_data (dict): the JSON object to convert
    """
    return pd.DataFrame(json_data)

def convert_gps_to_dataframe(json_data: dict) -> pd.DataFrame:
    """
    Convert a JSON object containing GPS data to a pandas DataFrame
    Args:
        json_data (dict): the JSON object to convert
    """

    df = pd.DataFrame(json_data)

    # Create additional columns for latitude and long
    df['latitude'] = df['coordinates'].apply(lambda x: x['latitude'])
    df['longitude'] = df['coordinates'].apply(lambda x: x['longitude'])

    # Drop the coordinates column
    df.drop(columns=['coordinates'], inplace=True)

    return df