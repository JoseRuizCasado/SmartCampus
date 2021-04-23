import requests
import json
import os
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import sleep


USER = "***"
PASSWORD = "***"
SERVICE = "***"
SERVICE_PATH = "***"
ORION_HOST = "***"

warnings.simplefilter('ignore',InsecureRequestWarning)


def get_token():
    """Generate token to authenticate in Smart Campus Fiware service.

    Returns:
      token.

    """
    url = 'https://'+ORION_HOST+':6001/v3/auth/tokens'
    headers = {'fiware-service': SERVICE, 'fiware-servicepath': SERVICE_PATH, 'Content-type': 'application/json'}

    payload={
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": SERVICE
                        },
                        "name": USER,
                        "password": PASSWORD
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                    "name": SERVICE
                    },
                    "name": SERVICE_PATH
                }
            }
        }
    }

    response=requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    response.encoding='utf-8'
    print("Status code: ", response.status_code)
    #print(response.text)
    print(response.headers["X-Subject-Token"])
    return response.headers["X-Subject-Token"]


def get_data():
    """Make request to Smart Campus Fiware service.

    Returns:
      Noise measured by the sensor.

    """
    token = get_token()
    url = 'https://'+ORION_HOST+':2026/v2/entities?id=plugsense:PS02'
    headers = {'fiware-service': SERVICE, 'fiware-servicepath': SERVICE_PATH, 'X-Auth-Token': token}  # Maybe the token changed
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    #print(response.text)
    response_dict=json.loads(response.text)
    print("Status code: ", response.status_code)
    # print(response.text)
    noise = response_dict[0]['NOISE']['value']
    datetime = response_dict[0]['NOISE']['metadata']['TimeInstant']['value']
    print(noise, datetime)
    return noise, datetime

