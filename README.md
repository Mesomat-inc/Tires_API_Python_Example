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
ACCESS_TOKEN = 'my_access_token'
REFRESH_TOKEN = 'my_refresh_token',
PASSWORD = 'my_password',
API_BASE_URL = 'https://driverapp.eastus.cloudapp.azure.com/
```

## Usage


To use this project, follow these steps:

1. **Run the Authentication Script**

    First, you need to run the `authentication.py` script to update the access and refresh token environment variables. Execute the following command:

    ```bash
    python authentication.py
    ```

2. **Call the API Script**

    After updating the tokens, you can call the `api_call.py` script. The specific function that will be executed is the one specified in the `__name__ == "__main__"` section of the code. Run the script with:

    ```bash
    python api_call.py
    ```


## License

Look into licensing