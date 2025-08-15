import requests
from app.admin.admin_client import get_admin_token
from app import config  # important pour accéder à KEYCLOAK_ADMIN_BASE_URL
from app.admin.admin_client import keycloak_admin_request

# ROLES REALM

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

def get_role_mappings(user_id: str):
    # Rôles Realm
    realm_roles = keycloak_admin_request(
        "GET", f"users/{user_id}/role-mappings/realm"
    )

    # Rôles Client → il faut d'abord récupérer la liste des clients
    clients = keycloak_admin_request("GET", "clients")

    client_roles_data = {}
    if clients:
        for client in clients:
            client_uuid = client["id"]
            roles = keycloak_admin_request(
                "GET", f"users/{user_id}/role-mappings/clients/{client_uuid}"
            )
            if roles:  # éviter les vides
                client_roles_data[client["clientId"]] = roles

    return {
        "realm_roles": realm_roles,
        "client_roles": client_roles_data
    }
def update_role_mappings(user_id: str, scope: str, roles: list, action: str):
    """
    Met à jour les mappings de rôles (realm ou client) pour un utilisateur.
    """
    # 1. Déterminer endpoint
    if scope == "realm":
        all_roles = keycloak_admin_request("GET", "roles")  # Liste des rôles realm
        endpoint = f"users/{user_id}/role-mappings/realm"
    else:
        # Chercher l'UUID du client
        clients = keycloak_admin_request("GET", "clients")
        if not clients:
            raise Exception("Impossible de récupérer la liste des clients.")
        
        client_match = next((c for c in clients if c["clientId"] == scope), None)
        if not client_match:
            raise Exception(f"Client '{scope}' introuvable.")
        
        client_uuid = client_match["id"]
        all_roles = keycloak_admin_request("GET", f"clients/{client_uuid}/roles")  # Liste des rôles client
        endpoint = f"users/{user_id}/role-mappings/clients/{client_uuid}"

    # 2. Mapper noms → objets complets
    roles_payload = []
    if not all_roles:
        raise Exception(f"Aucun rôle trouvé dans '{scope}'.")
    for role in roles:
        match = next((r for r in all_roles if r["name"] == role["name"]), None)
        if not match:
            raise Exception(f"Rôle '{role['name']}' introuvable dans '{scope}'.")
        roles_payload.append({
            "id": match["id"],
            "name": match["name"]
        })

    # 3. Méthode HTTP selon action
    method = "POST" if action == "add" else "DELETE"
    
    # 4. Appel API Keycloak
    return keycloak_admin_request(method, endpoint, json=roles_payload)

# ROLES CLIENT

def create_client_role(client_id: str, role_data: dict):
    """
    Crée un rôle pour un client donné (client_id = 'my-client')
    """
    # Récupérer UUID du client
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")
    
    client_uuid = client_match["id"]

    # Création du rôle client
    endpoint = f"clients/{client_uuid}/roles"
    return keycloak_admin_request("POST", endpoint, json=role_data)


def list_client_roles(client_id: str):
    """
    Liste tous les rôles d'un client donné
    """
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")

    client_uuid = client_match["id"]
    endpoint = f"clients/{client_uuid}/roles"
    return keycloak_admin_request("GET", endpoint)


def update_client_role(client_id: str, role_name: str, role_data: dict):
    """
    Met à jour un rôle d'un client
    """
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")

    client_uuid = client_match["id"]

    # Récupérer le rôle existant
    existing_role = keycloak_admin_request("GET", f"clients/{client_uuid}/roles/{role_name}")
    if not existing_role:
        raise Exception(f"Rôle '{role_name}' introuvable pour le client '{client_id}'.")

    updated_role = {**existing_role, **role_data}
    endpoint = f"clients/{client_uuid}/roles/{role_name}"
    return keycloak_admin_request("PUT", endpoint, json=updated_role)


def delete_client_role(client_id: str, role_name: str):
    """
    Supprime un rôle d'un client
    """
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")

    client_uuid = client_match["id"]
    endpoint = f"clients/{client_uuid}/roles/{role_name}"
    return keycloak_admin_request("DELETE", endpoint)


def assign_client_roles_to_user(user_id: str, client_id: str, role_names: list[str]):
    """
    Assigne une liste de rôles client à un utilisateur.
    """
    # 1. Récupérer UUID du client
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")
    client_uuid = client_match["id"]

    # 2. Récupérer les infos complètes des rôles
    client_roles = keycloak_admin_request("GET", f"clients/{client_uuid}/roles")
    if not client_roles:
        raise Exception(f"Aucun rôle trouvé pour le client '{client_id}'.")
    roles_payload = []
    for role_name in role_names:
        match = next((r for r in client_roles if r["name"] == role_name), None)
        if not match:
            raise Exception(f"Rôle '{role_name}' introuvable pour le client '{client_id}'.")
        roles_payload.append({
            "id": match["id"],
            "name": match["name"]
        })

    # 3. Assigner les rôles
    endpoint = f"users/{user_id}/role-mappings/clients/{client_uuid}"
    return keycloak_admin_request("POST", endpoint, json=roles_payload)


def remove_client_roles_from_user(user_id: str, client_id: str, role_names: list[str]):
    """
    Retire une liste de rôles client à un utilisateur.
    """
    clients = keycloak_admin_request("GET", "clients")
    if not clients:
        raise Exception("Impossible de récupérer la liste des clients.")
    client_match = next((c for c in clients if c["clientId"] == client_id), None)
    if not client_match:
        raise Exception(f"Client '{client_id}' introuvable.")
    client_uuid = client_match["id"]

    # Récupérer les infos des rôles
    client_roles = keycloak_admin_request("GET", f"clients/{client_uuid}/roles")
    if not client_roles:
        raise Exception(f"Aucun rôle trouvé pour le client '{client_id}'.")
    roles_payload = []
    for role_name in role_names:
        match = next((r for r in client_roles if r["name"] == role_name), None)
        if not match:
            raise Exception(f"Rôle '{role_name}' introuvable pour le client '{client_id}'.")
        roles_payload.append({
            "id": match["id"],
            "name": match["name"]
        })

    # Supprimer les rôles
    endpoint = f"users/{user_id}/role-mappings/clients/{client_uuid}"
    return keycloak_admin_request("DELETE", endpoint, json=roles_payload)
