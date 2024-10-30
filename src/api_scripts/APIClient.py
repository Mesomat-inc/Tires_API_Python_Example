import requests
from requests import exceptions
import os
import json
import pandas as pd
from dotenv import load_dotenv

from utils import (
    is_iso_8601,
    update_dotenv_key,
    convert_sensor_data_to_dataframe,
    convert_gps_to_dataframe,
)



BASE_URL = os.getenv("API_BASE_URL", "https://driverapp.eastus.cloudapp.azure.com/")
FLEET_URL = BASE_URL + "v1/fleet/"

#load_dotenv(override=True)

class APIClient:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.access_token = os.getenv("ACCESS_TOKEN", None)
        self.refresh_token = os.getenv("REFRESH_TOKEN", None)

        if not self.access_token or not self.refresh_token:
            self._authenticate()

    def _authenticate(self):
        """
        Authenticate the user using the email and password in .env file
        """

        url_token = BASE_URL + "/auth/token"

        params = {"email": self.email, "password": self.password}

        token = requests.post(url_token, params=params)

        if token:

            self.access_token = token.json()["access_token"]
            self.refresh_token = token.json()["refresh_token"]
            print("Authentication successful")

            # update the refresh token in the .env file
            update_dotenv_key("REFRESH_TOKEN", self.refresh_token)

            # update the access token in the .env file
            update_dotenv_key("ACCESS_TOKEN", self.access_token)

            return {
                "access_token": token.json()["access_token"],
                "refresh_token": token.json()["refresh_token"],
            }
        else:
            print(f"Failed to send request: {token.json()}")

    def format_header(self):
        return {"token": self.access_token}

    def refresh_access_token(self):
        """
        Refresh the access token using the refresh token in the .env file
        """

        url_token = BASE_URL + "/auth/refresh-token"

        params = {
            "email": os.getenv("USER_EMAIL"),
            "refresh_token": os.getenv("REFRESH_TOKEN"),
        }

        
        token = requests.post(url_token, params=params)
        
       
        if token:

            self.access_token = token.json()["access_token"]
            self.refresh_token = token.json()["refresh_token"]

            # update the access token in the .env file
            update_dotenv_key("ACCESS_TOKEN", self.access_token)

            # reload the .env file
            load_dotenv(override=True)

            return {
                "access_token": token.json()["access_token"],
            }
        else:
            raise requests.exceptions.HTTPError("Failed to refresh access token")

    def api_request(self, endpoint, params=None):
        """
        Make a request to the API endpoint, if the request fails due to an expired token,
        the access token will be refreshed and the request will be retried.

        params is optional and can be used to pass query parameters to the request
        """

        headers = self.format_header()

        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 401:  # Unauthorized
            print("Token expired, refreshing...")
            try:
                response = self.refresh_access_token()
            except exceptions.HTTPError as e:
                print('Failed to refresh token, trying to re-authenticate with email and password')
                self._authenticate()

            # Retry with new token
            headers = self.format_header()
            response = requests.get(endpoint, headers=headers)

        # Handle other potential errors or raise if failed
        if response.status_code == 404:
            print(f'Could not find the requested resource: {response.json()["detail"]}')
            return None
        elif response.status_code == 401:
            raise requests.exceptions.HTTPError(
                f"{response.status_code} Client Error: {response.json()['detail']}"
            )
        else:     
            response.raise_for_status()
        
        return response.json()

    def get_asset_list(self) -> list[dict]:
        """
        Get the list of assets with their information
        """

        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "assets"

        # make the request
        response = self.api_request(url)

        return response

    def get_asset_info(self, gateway_id) -> dict:
        """
        Get the information of a specific asset
        Args:
            gateway_id (int): the id of the gateway (shown on the gateway sticker)
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "assets/" + str(gateway_id)

        # make the request
        response = self.api_request(url)

        return response

    def get_sensors_attached_to_asset(self, gateway_id) -> list[dict]:
        """
        Get the list of sensors attached to an asset
        Args:
            gateway_id (int): the id of the gateway (shown on the gateway sticker)
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "assets/" + str(gateway_id) + "/sensors"

        # make the request
        response = self.api_request(url)

        return response

    def get_sensor_data_by_asset(
        self, gateway_id, start_time, end_time=None
    ) -> pd.DataFrame:
        """
        Get the data of a all sensors attached to an asset, note the maximum number of
        records returned is capped. The maximum number of records corresponds to 1 day of data 
        for a single sensor assuming a 1 minute sampling rate.
        Args:
            gateway_id (int): the id of the gateway (shown on the gateway sticker)
            start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM,
            end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "assets/" + str(gateway_id) + "/sensors/stats"

        # parameters for the request
        if end_time is None and is_iso_8601(start_time):
            params = {"start_time": start_time}
        elif is_iso_8601(start_time) and is_iso_8601(end_time):
            params = {"start_time": start_time, "end_time": end_time}
        else:
            raise ValueError("Invalid timestamp format")

        # make the request
        response = self.api_request(url, params=params)

        # convert the response to a DataFrame
        # this is optional, you can return the response as a json object
        response_df = convert_sensor_data_to_dataframe(response)

        return response_df

    def get_gps_by_asset(
        self, gateway_id, start_time, end_time=None, undersampling_factor=30
    ) -> pd.DataFrame:
        """
        Get the GPS data of an asset, note the maximum number of
        records is capped. The maximum number of records corresponds to 1 day of gps data
        assuming 1 minute sampling rate (undersampling_factor = 30).
        Args:
            gateway_id (int): the id of the gateway (shown on the sticker)
            start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
            end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
            undersampling_factor (int) - Optional: the factor to undersample the data, default is 30
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "assets/" + str(gateway_id) + "/gps"

        # parameters for the request
        if end_time is None and is_iso_8601(start_time):
            params = {"start_time": start_time}
        elif is_iso_8601(start_time) and is_iso_8601(end_time):
            params = {"start_time": start_time, "end_time": end_time}
        else:
            raise ValueError("Invalid timestamp format")

        # add the undersampling factor if provided, otherwise the default is 30
        if undersampling_factor:
            params["undersampling_factor"] = undersampling_factor

        # make the request
        response = self.api_request(url, params=params)

        # convert the response to a DataFrame
        # this is optional, you can return the response as a json object
        response_df = convert_gps_to_dataframe(response)

        return response_df

    def get_sensor_info_by_id(self, sensor_id) -> dict:
        """
        Get the information of a specific sensor,
        Args:
            sensor_id (int): the serial number of the sensor
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "sensors/" + str(sensor_id)

        # make the request
        response = self.api_request(url)

        return response

    def get_sensor_data_by_id(
        self, sensor_id, start_time, end_time=None
    ) -> pd.DataFrame:
        """
        Get the statistics of a specific sensor, note the maximum number of
        records is is capped. The maximum number of records corresponds to 1 day of data 
        for a single sensor assuming a 1 minute sampling rate.
        Args:
            sensor_id (int): the serial number of the sensor
            start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
            end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "sensors/" + str(sensor_id) + "/stats"

        # parameters for the request
        if end_time is None and is_iso_8601(start_time):
            params = {"start_time": start_time}
        elif is_iso_8601(start_time) and is_iso_8601(end_time):
            params = {"start_time": start_time, "end_time": end_time}
        else:
            raise ValueError("Invalid timestamp format")

        # make the request
        response = self.api_request(url, params=params)

        # convert sensor data to dataframe
        # this is optional, you can return the response as a json object
        response_df = convert_sensor_data_to_dataframe(response)

        return response_df

    def get_latest_sensor_data_by_id(self, sensor_id) -> dict:
        """
        Get the latest statistics of a specific sensor
        Args:
            sensor_id (int): the serial number of the sensor
        """
        # create the url for the request, refer to the API documentation for the correct endpoint
        url = FLEET_URL + "sensors/" + str(sensor_id) + "/stats/latest"

        # make the request
        response = self.api_request(url)

        return response
