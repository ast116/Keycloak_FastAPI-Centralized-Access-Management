import requests
from app.admin.admin_client import get_admin_token
from app import config  # important pour accéder à KEYCLOAK_ADMIN_BASE_URL
from app.admin.admin_client import keycloak_admin_request

def create_role(role_data: dict):
    token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"{config.KEYCLOAK_ADMIN_BASE_URL}/roles"
    response = requests.post(url, json=role_data, headers=headers)
    if response.status_code not in (201, 204):
        raise Exception(f"Erreur création rôle: {response.status_code} - {response.text}")
    return {"message": "Rôle créé avec succès"}


def list_roles():
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.KEYCLOAK_ADMIN_BASE_URL}/roles"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erreur récupération rôles: {response.status_code} - {response.text}")
    return response.json()

def update_role(role_name: str, role_data: dict):
    token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Récupérer le rôle existant
    get_url = f"{config.KEYCLOAK_ADMIN_BASE_URL}/roles/{role_name}"
    existing_role_resp = requests.get(get_url, headers=headers)
    if existing_role_resp.status_code != 200:
        raise Exception(f"Erreur récupération rôle: {existing_role_resp.status_code} - {existing_role_resp.text}")

    existing_role = existing_role_resp.json()

    # 2. Fusionner les données
    updated_role = {**existing_role, **role_data}

    # 3. Envoyer l'objet complet
    put_url = f"{config.KEYCLOAK_ADMIN_BASE_URL}/roles/{role_name}"
    response = requests.put(put_url, json=updated_role, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Erreur mise à jour rôle: {response.status_code} - {response.text}")

    return {"message": "Rôle mis à jour avec succès"}

def delete_role(role_name: str):
    """
    Supprime un rôle existant
    """
    token = get_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.KEYCLOAK_ADMIN_BASE_URL}/roles/{role_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code not in (204,):
        raise Exception(f"Erreur suppression rôle: {response.status_code} - {response.text}")
    return {"message": "Rôle supprimé avec succès"}

def get_realm_role_by_name(role_name: str):
    endpoint = f"roles/{role_name}"
    return keycloak_admin_request("GET", endpoint)
def assign_roles_to_user(user_id: str, role_names: list[str]):
    """
    Récupère les infos complètes des rôles et les assigne à l'utilisateur.
    """
    roles_to_assign = []
    for role_name in role_names:
        # Récupération du rôle par son nom
        role_info = keycloak_admin_request("GET", f"roles/{role_name}")
        if not role_info or "id" not in role_info:
            raise Exception(f"Role '{role_name}' introuvable dans Keycloak")
        roles_to_assign.append(role_info)

    # Attribution des rôles à l'utilisateur
    endpoint = f"users/{user_id}/role-mappings/realm"
    return keycloak_admin_request("POST", endpoint, json=roles_to_assign)


def remove_roles_from_user(user_id: str, role_names: list[str]):
    """
    Récupère les infos complètes des rôles et les retire à l'utilisateur.
    """
    roles_to_remove = []
    for role_name in role_names:
        role_info = keycloak_admin_request("GET", f"roles/{role_name}")
        if not role_info or "id" not in role_info:
            raise Exception(f"Role '{role_name}' introuvable dans Keycloak")
        roles_to_remove.append(role_info)

    # Suppression des rôles
    endpoint = f"users/{user_id}/role-mappings/realm"
    return keycloak_admin_request("DELETE", endpoint, json=roles_to_remove)

