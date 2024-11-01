from APIClient import APIClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv(override=True)


def main():
    """
    This function is the entry point of the script. It creates an instance of the APIClient
    and makes a request to the API. The Client will automatically authenticate using the
    email and password stored in the .env file.

    Note: if the .env file contains an access token and a refresh token, the client will try to use
    them to authenticate. If the access token has expired, the client will automatically refresh it.
    In the case of an invalid refresh token, the client will try to re-authenticate using the email and password 
    stored in the .env file. If successful, the new access token and refresh token will be updated in the .env file.

    To run an api request, you can update the code in this function to make a request to the API.
    See the APIClient.py file for the available methods and the expected parameters.

    """

    # Create an instance of the APIClient
    api_client = APIClient(
        email=os.getenv("USER_EMAIL"), password=os.getenv("PASSWORD")
    )

    # Make a request to the API
    asset_list = api_client.get_asset_list()
    print(f"the assets in your fleet are: {asset_list}")

    first_asset = asset_list[0]
    sensor_list = api_client.get_sensors_attached_to_asset(first_asset["gateway_id"])
    print(f"the sensors attached to this asset are: {sensor_list}")

    # Define the time range for the data request
    start_time_str = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    end_time_str = datetime.now(timezone.utc).isoformat()

    example_sensor = sensor_list[0]

    # Get sensor data, returns a pandas DataFrame
    sensor_data = api_client.get_sensor_data_by_id(
        example_sensor["sensor_id"],
        start_time = start_time_str
    )
    print(f"Some sensor data for this asset is: {sensor_data}")

    # Get GPS data for the asset, returns a pandas DataFrame
    df_gps = api_client.get_gps_by_asset(
        first_asset["gateway_id"],
        start_time = start_time_str,
        end_time= end_time_str,
        undersampling_factor=30,
    )
    print(f"Some gps data for this asset is: {df_gps}")



if __name__ == "__main__":
    main()
