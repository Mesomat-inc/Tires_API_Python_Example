import requests
import os
from dotenv import load_dotenv
from authentication import refresh_access_token
from utils import format_headers, is_iso_8601, convert_json_to_dataframe

load_dotenv(override=True)

# URL for the API endpoint
FLEET_URL = os.getenv('API_BASE_URL', 'https://driverapp.eastus.cloudapp.azure.com/') + 'v1/fleet/'

def get_vehicle_list() -> requests.Response:

    ''' 
    Get the list of vehicles with their information
    '''

    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles'

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

def get_vehicle_info(vehicle_id) -> requests.Response:

    '''
    Get the information of a specific vehicle
    Args:
        vehicle_id (int): the id of the vehicle
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles/' + str(vehicle_id)

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

def get_sensors_attached_to_vehicle(vehicle_id) -> requests.Response:

    '''
    Get the list of sensors attached to a vehicle
    Args:
        vehicle_id (int): the id of the vehicle
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles/' + str(vehicle_id) + '/sensors'

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

def get_sensor_data_by_vehicle(vehicle_id, start_time, end_time = None) -> requests.Response:

    '''
    Get the data of a all sensors attached to a vehicle, note the maximum number of 
    records returned is 1000
    Args:
        vehicle_id (int): the id of the vehicle
        start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM,
        end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles/' + str(vehicle_id) + '/sensors/stats'

    # parameters for the request
    if end_time is None and is_iso_8601(start_time):
        params = {
            'start_time': start_time
        }
    elif is_iso_8601(start_time) and is_iso_8601(end_time):
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
    else:
        raise ValueError('Invalid timestamp format')

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers, params=params)

    return response

def get_gps_by_vehicle(vehicle_id, start_time, end_time = None, undersampling_factor = 30) -> requests.Response:

    '''
    Get the GPS data of a vehicle, note the maximum number of 
    records is 1000
    Args:
        vehicle_id (int): the id of the vehicle
        start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
        end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
        undersampling_factor (int) - Optional: the factor to undersample the data, default is 30
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'vehicles/' + str(vehicle_id) + '/gps'

    # parameters for the request
    if end_time is None and is_iso_8601(start_time):
        params = {
            'start_time': start_time
        }
    elif is_iso_8601(start_time) and is_iso_8601(end_time):
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
    else:
        raise ValueError('Invalid timestamp format')

    # add the undersampling factor if provided, otherwise the default is 30
    if undersampling_factor:
        params['undersampling_factor'] = undersampling_factor

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers, params=params)

    return response

def get_sensor_info_by_id(sensor_id) -> requests.Response:

    '''
    Get the information of a specific sensor, 
    Args:
        sensor_id (int): the serial number of the sensor
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'sensors/' + str(sensor_id)

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response

def get_sensor_data_by_id(sensor_id, start_time, end_time = None) -> requests.Response:
    
    '''
    Get the statistics of a specific sensor, note the maximum number of 
    records is 1000
    Args:
        sensor_id (int): the serial number of the sensor
        start_time (str): the start time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
        end_time (str) - Optional: the end time of the data in ISO 8601 format YYYY-MM-DDTHH:MM:SS+HH:MM
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'sensors/' + str(sensor_id) + '/stats'

    # parameters for the request
    if end_time is None and is_iso_8601(start_time):
        params = {
            'start_time': start_time
        }
    elif is_iso_8601(start_time) and is_iso_8601(end_time):
        params = {
            'start_time': start_time,
            'end_time': end_time
        }
    else:
        raise ValueError('Invalid timestamp format')

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers, params=params)

    return response

def get_latest_sensor_data_by_id(sensor_id) -> requests.Response:

    '''
    Get the latest statistics of a specific sensor
    Args:
        sensor_id (int): the serial number of the sensor
    '''
    # create the url for the request, refer to the API documentation for the correct endpoint
    url = FLEET_URL + 'sensors/' + str(sensor_id) + '/stats/latest'

    # automatically puts the JWT token in the headers with the right format
    headers = format_headers()

    # make the request
    response = requests.get(url, headers=headers)

    return response
    
if __name__ == '__main__':

    # call the desidered function here
    response = get_sensor_data_by_id(300, '2024-09-10T15:30:00+01:00')

    #response = get_vehicle_info(153)
    #display the response in the console
    print((response.json()))

    if response.status_code == 401:
        # if the token is expired, refresh it
        refresh_access_token()

        #reload environment variables to get the new token
        load_dotenv(override=True)

        # make the request again
        response = get_vehicle_list()

        #display the response in the console
        print(response.json())

    # this is optional and can be commented out
    # this is most useful for GPS and sensor data
    if response.status_code == 200:
        # convert the response to a pandas DataFrame
        df = convert_json_to_dataframe(response.json())
        print(df)