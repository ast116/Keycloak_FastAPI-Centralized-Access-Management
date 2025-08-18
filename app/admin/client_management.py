from app.admin.admin_client import keycloak_admin_request

def create_client(client_data: dict):
    """
    Crée un nouveau client Keycloak.
    client_data doit contenir au minimum : clientId, redirectUris, secret, publicClient, etc.
    """
    endpoint = "clients"
    response = keycloak_admin_request("POST", endpoint, data=client_data)
    return {"message": "Client créé avec succès", "details": response}


def list_clients():
    """
    Récupère la liste de tous les clients Keycloak.
    """
    endpoint = "clients"
    return keycloak_admin_request("GET", endpoint)


def update_client(client_id: str, update_data: dict):
    """
    Met à jour un client existant.
    """
    endpoint = f"clients/{client_id}"
    keycloak_admin_request("PUT", endpoint, data=update_data)
    return {"message": "Client mis à jour avec succès"}


def delete_client(client_id: str):
    """
    Supprime un client Keycloak.
    """
    endpoint = f"clients/{client_id}"
    keycloak_admin_request("DELETE", endpoint)
    return {"message": "Client supprimé avec succès"}
