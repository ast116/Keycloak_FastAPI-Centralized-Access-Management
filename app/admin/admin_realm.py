from typing import Optional
from app.admin.admin_master import keycloak_master_request
from app.admin.admin_client import keycloak_admin_request
from app.models.realm import RealmCreateRequest, RealmUpdateRequest


def create_realm(data: RealmCreateRequest):
    """
    Crée un nouveau realm dans Keycloak via l'Admin API
    """
    payload = {
        "realm": data.realm_name,
        "enabled": data.enabled,
        "displayName": data.display_name,
        "sslRequired": data.ssl_required,
        "registrationAllowed": data.registration_allowed,
        "loginWithEmailAllowed": data.login_with_email_allowed,
        "bruteForceProtected": data.brute_force_protected
    }
    
    if data.password_policy:
        payload["passwordPolicy"] = data.password_policy

    # Appel de Keycloak Admin REST API pour créer le realm
    return keycloak_master_request("POST", "realms", json=payload)

def update_realm(realm_name: str, data: RealmUpdateRequest):
    """
    Met à jour les paramètres d'un realm existant
    """
    # Mapping correct des noms de champs attendus par Keycloak
    payload = {}
    if data.enabled is not None:
        payload["enabled"] = data.enabled
    if data.display_name is not None:
        payload["displayName"] = data.display_name
    if data.ssl_required is not None:
        payload["sslRequired"] = data.ssl_required
    if data.registration_allowed is not None:
        payload["registrationAllowed"] = data.registration_allowed
    if data.login_with_email_allowed is not None:
        payload["loginWithEmailAllowed"] = data.login_with_email_allowed
    if data.password_policy is not None:
        payload["passwordPolicy"] = data.password_policy
    if data.brute_force_protected is not None:
        payload["bruteForceProtected"] = data.brute_force_protected

    if not payload:
        raise ValueError("Aucun champ à mettre à jour fourni")

    endpoint = f"realms/{realm_name}"
    return keycloak_master_request("PUT", endpoint, json=payload)



def delete_realm(realm_name: str):
    """
    Supprime un realm existant dans Keycloak
    """
    endpoint = f"realms/{realm_name}"
    return keycloak_master_request("DELETE", endpoint)
