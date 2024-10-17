import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()


BASE_URL = os.getenv("API_BASE_URL", "https://driverapp.eastus.cloudapp.azure.com/")


def authenticate():
    url_token = BASE_URL + "/auth/token"

    params = {"email": os.getenv("USER_EMAIL"), "password": os.getenv("PASSWORD")}

    token = requests.post(url_token, params=params)

    if token:
        return {
            "access_token": token.json()["access_token"],
            "refresh_token": token.json()["refresh_token"],
        }
    else:
        print(f"Failed to send request: {token.json()}")


def refresh_access_token():
    url_token = BASE_URL + "/auth/refresh-token"

    params = {
        "email": os.getenv("USER_EMAIL"),
        "refresh_token": os.getenv("REFRESH_TOKEN"),
    }

    token = requests.post(url_token, params=params)

    if token:
        update_dotenv_key("ACCESS_TOKEN", token.json()["access_token"])
        return {
            "access_token": token.json()["access_token"],
        }


def update_dotenv_key(key, value):
    set_key(".env", key, value)
    print(f"{key} was updated")


if __name__ == "__main__":

    token_dict = authenticate()

    access_token = os.getenv("ACCESS_TOKEN")
    refresh_token = os.getenv("REFRESH_TOKEN")

    if token_dict:
        if access_token:
            update_dotenv_key("ACCESS_TOKEN", token_dict["access_token"])
        if refresh_token:
            update_dotenv_key("REFRESH_TOKEN", token_dict["refresh_token"])
