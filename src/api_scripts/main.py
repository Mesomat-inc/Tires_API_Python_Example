from APIClient import APIClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    """
    This function is the entry point of the script. It creates an instance of the APIClient
    and makes a request to the API. The Client will automatically authenticate using the
    email and password stored in the .env file.

    Note: if the .env file contains an access token and a refresh token, the client will try to use
    them to authenticate. If the access token has expired, the client will automatically refresh it.
    You will be notified if the refresh token has expired or is invalid with the following error:
    requests.exceptions.HTTPError: 401 Client Error, in which case it is recommended to
    clear both the access token and the refresh token from the .env file and run the script again.

    To run an api request, you can update the code in this function to make a request to the API.
    See the APIClient.py file for the available methods and the expected parameters.

    """

    # Create an instance of the APIClient
    api_client = APIClient(
        email=os.getenv("USER_EMAIL"), password=os.getenv("PASSWORD")
    )

    # Make a request to the API
    response = api_client.get_gps_by_vehicle(
        153,
        start_time="2024-09-10T15:30:00",
        end_time="2024-09-10T15:40:00",
        undersampling_factor=1,
    )
    print(response)


if __name__ == "__main__":
    main()
