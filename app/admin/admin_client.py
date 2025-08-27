# app/admin/admin_client.py

import requests
from app import config

def get_admin_token():
    """
    Récupère un token admin depuis Keycloak via le client fastapi-admin.
    """
    data = {
        "client_id": config.KEYCLOAK_ADMIN_CLIENT_ID,
        "client_secret": config.KEYCLOAK_ADMIN_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }

    response = requests.post(config.KEYCLOAK_ADMIN_TOKEN_URL, data=data)

    if response.status_code != 200:
        raise Exception(f"Erreur récupération token admin: {response.text}")

    return response.json()["access_token"]


def keycloak_admin_request(method: str, url: str, data=None, json=None):
    token = get_admin_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.request(method, url, headers=headers, data=data, json=json)

    if not response.ok:
        raise Exception(f"Erreur API Keycloak: {response.status_code} - {response.text}")
    return response.json() if response.text else {}

