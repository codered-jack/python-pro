import requests
from datetime import datetime
# https://pixe.la/

pixela_endpoint = "https://pixe.la/v1/users"
USERNAME = "coderedjack"
TOKEN = "hjknsa4ghdst243bdb3544"
GRAPH_ID = "graph3544"

user_parans = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_parans)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Coding",
    "unit": "days",
    "type": "int",
    "color": "ajisai",
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint= f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"

today = datetime.now()

pixela_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "3",
}

# response = requests.post(url=pixel_creation_endpoint, json=pixela_data, headers=headers)
# print(response.text)