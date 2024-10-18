# Tires API Python Example

This project demonstrates how to interact with the Tires API using Python.

## Setup

### Create a Virtual Environment

To create a virtual environment, run the following command:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On Windows:
    ```bash
    .venv\Scripts\activate
    ```
- On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

### Install Packages

Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory of the project and enter your credentials. You can use the `.example.env` file as a template.

Example `.env` file:

```
USER_EMAIL = 'john.doe@domain.com'
PASSWORD = 'my_password',
API_BASE_URL = 'https://driverapp.eastus.cloudapp.azure.com/
```

Access token and refresh token will automatically be added to the .env file upon first authentication.
These variables can also be entered manually in the `.env` if known. If the refresh token is expired or invalid,
the user will be notified with the following error:

```bash
requests.exceptions.HTTPError: 401 Client Error
```

In this case, it is recommended to clear the value of both token in the `.env` file which will force the
client to authenticate and regenerate the tokens.

## Usage

To use this project, follow these steps:

1. **Navigate to the api_scripts module**
    ```bash
    cd src\api_scripts\
    ```

2. **APIClient Class**

    All methods to interact with the API are stored in the APIClient Class, including authnetication methods.
    Each route documented in https://driverapp.eastus.cloudapp.azure.com/docs#/ has a corresponding method in the
    APIClient class.

3. **Call the API Script**

    The API should be called using `src\api_scripts\main.py`. The code in the main function can be modified to 
    call one of the methods available in the APIClient class. For example:

    ```bash
    # Create an instance of the APIClient
    api_client = APIClient(
        email=os.getenv("USER_EMAIL"),
        password=os.getenv("PASSWORD")
    )
    
    # Make a request to the API
    response = api_client.get_gps_by_vehicle(153, start_time= "2024-09-10T15:30:00", end_time= "2024-09-10T15:40:00", undersampling_factor=1)
    print(response)
    ```


## License

Look into licensing