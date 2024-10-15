import requests
import os
from dotenv import load_dotenv
from authentication import refresh_access_token

if __name__ == '__main__':
    

    # headers = {
    #     'Authorization': 'Bearer ' + os.getenv('ACCESS_TOKEN')
    # }
    # response = requests.get(url, headers=headers)
    # if response.status_code == 401:
    #     refresh_access_token()
    #     headers = {
    #         'Authorization': 'Bearer ' + os.getenv('ACCESS_TOKEN')
    #     }
    #     response = requests.get(url, headers=headers)
    # print(response.json())