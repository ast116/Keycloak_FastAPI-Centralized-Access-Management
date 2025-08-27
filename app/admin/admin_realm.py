from typing import Optional
from app.admin.admin_master import keycloak_master_request
from app.admin.admin_client import keycloak_admin_request
from app.models.realm import RealmCreateRequest


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

