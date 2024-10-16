import requests
import os
from dotenv import load_dotenv
from authentication import refresh_access_token

load_dotenv(override=True)

# URL for the API endpoint
FLEET_URL = os.getenv('API_BASE_URL', 'https://driverapp.eastus.cloudapp.azure.com/') + 'v1/fleet/'

def format_headers():
    return {'token': os.getenv('ACCESS_TOKEN')}

def get_vehicle_list():

    # reate the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles'

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

def get_vehicle_info(vehicle_id):

    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles/' + str(vehicle_id)

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

if __name__ == '__main__':


    response = get_vehicle_info(151)

    print(response.json())
    if response.status_code == 401:
        # if the token is expired, refresh it
        refresh_access_token()

        # make the request again
        response = get_vehicle_list()
        print(response.json())

   