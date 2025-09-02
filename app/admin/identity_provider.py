from app.admin.admin_client import keycloak_admin_request
from app import config

def create_identity_provider(data):
    """
    Crée un Identity Provider externe dans Keycloak.
    """
    url = f"identity-provider/instances"
    
    payload = {
        "alias": data.alias,
        "providerId": data.provider_id,
        "enabled": data.enabled,
        "trustEmail": data.trust_email,
        "storeToken": data.store_token,
        "linkOnly": data.link_only,
        "config": data.config
    }

    return keycloak_admin_request("POST", url, json=payload)


def update_identity_provider(alias: str, data):
    """
    Met à jour la configuration d’un Identity Provider.
    """
    url = f"identity-provider/instances/{alias}"

    payload = {}
    if data.enabled is not None:
        payload["enabled"] = data.enabled
    if data.trust_email is not None:
        payload["trustEmail"] = data.trust_email
    if data.store_token is not None:
        payload["storeToken"] = data.store_token
    if data.link_only is not None:
        payload["linkOnly"] = data.link_only
    if data.config is not None:
        payload["config"] = data.config

    return keycloak_admin_request("PUT", url, json=payload)


def delete_identity_provider(alias: str):
    """
    Supprime un Identity Provider.
    """
    url = f"identity-provider/instances/{alias}"
    return keycloak_admin_request("DELETE", url)

def list_identity_providers():
    """
    Récupère la liste des Identity Providers d’un realm.
    """
    url = f"identity-provider/instances"
    return keycloak_admin_request("GET", url)
