from APIClient import APIClient
import os

def main():

    # Create an instance of the APIClient, passing the required parameters
    # the email and password are stored in the .env file and the client will
    # automatically authenticate
    api_client = APIClient(
        email=os.getenv("USER_EMAIL"),
        password=os.getenv("PASSWORD")
    )
    
    # Make a request to the API
    #response = api_client.get_sensor_data_by_id(300, "2024-09-10T15:30:00+01:00")
    response = api_client.get_latest_sensor_data_by_id(300)
    print(response)




if __name__ == "__main__":  
    main()
    