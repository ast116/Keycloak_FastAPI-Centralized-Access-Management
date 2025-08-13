# app/admin/user_management.py

from app.admin.admin_client import keycloak_admin_request
from typing import Optional

def create_user(username, email, first_name="", last_name=""):
    payload = {
        "username": username,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "enabled": True,
        "emailVerified": True
    }
    return keycloak_admin_request("POST", "users", json=payload)


def list_users():
    return keycloak_admin_request("GET", "users")


def get_user_by_id(user_id):
    return keycloak_admin_request("GET", f"users/{user_id}")


def delete_user(user_id):
    return keycloak_admin_request("DELETE", f"users/{user_id}")

def update_user(user_id: str, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None):
    payload = {}
    if email is not None:
        payload["email"] = email
    if first_name is not None:
        payload["firstName"] = first_name
    if last_name is not None:
        payload["lastName"] = last_name

    if not payload:
        return {"message": "Aucun champ à mettre à jour."}

    return keycloak_admin_request("PUT", f"users/{user_id}", json=payload)


def reset_password(user_id, new_password):
    payload = {
        "type": "password",
        "value": new_password,
        "temporary": False
    }
    return keycloak_admin_request("PUT", f"users/{user_id}/reset-password", json=payload)
