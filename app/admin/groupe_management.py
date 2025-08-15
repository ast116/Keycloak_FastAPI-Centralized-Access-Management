# app/admin/groupe_management.py
from typing import List, Dict, Optional
from app.admin.admin_client import keycloak_admin_request
from app import config 

def create_group(group_data: dict):
    """
    group_data = {"name": "nom_du_groupe", "description": "texte optionnel"}
    """
    return keycloak_admin_request("POST", "groups", json=group_data)


def list_groups():
    return keycloak_admin_request("GET", "groups")


def update_group(group_id: str, group_data: dict):
    """
    group_data = {"name": "nouveau_nom", "description": "nouvelle description"}
    """
    return keycloak_admin_request("PUT", f"groups/{group_id}", json=group_data)

def delete_group(group_id: str):
    return keycloak_admin_request("DELETE", f"groups/{group_id}")

def add_user_to_group(user_id: str, group_id: str):
    """
    Ajoute un utilisateur au groupe (via l'API correcte Keycloak).
    """
    endpoint = f"users/{user_id}/groups/{group_id}"
    # Keycloak renvoie 204 No Content
    keycloak_admin_request("PUT", endpoint)
    return {"message": "Utilisateur ajouté au groupe"}

def remove_user_from_group(user_id: str, group_id: str):
    """
    Retire un utilisateur du groupe (via l'API correcte Keycloak).
    """
    endpoint = f"users/{user_id}/groups/{group_id}"
    keycloak_admin_request("DELETE", endpoint)
    return {"message": "Utilisateur retiré du groupe"}
