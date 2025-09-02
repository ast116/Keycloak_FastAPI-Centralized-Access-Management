import requests
from app import config

def get_master_admin_token(username: str = "admin_dev", password: str = "admin123"):
    """
    Récupère un token admin pour le realm master (admin-cli)
    """
    data = {
        "client_id": "admin-cli",
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    url = f"{config.KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token"
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def keycloak_master_request(method, endpoint, **kwargs):
    """
    Envoie une requête à l'Admin REST API de Keycloak sur le realm master avec admin-cli
    """
    token = get_master_admin_token()  # récupère le token master
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"{config.KEYCLOAK_SERVER_URL}/admin/{endpoint}"  # pas de /realms/{realm} ici
    response = requests.request(method, url, headers=headers, **kwargs)

    if not response.ok:
        raise Exception(f"Erreur API Keycloak: {response.status_code} - {response.text}")

    return response.json() if response.text else None
