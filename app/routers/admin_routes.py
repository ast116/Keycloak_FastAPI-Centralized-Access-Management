from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app import config
from app.admin import client_management, user_management
from app.admin.admin_client import keycloak_admin_request
from app.admin import admin_realm
from app.admin.audit_management import export_events_csv, list_events
from app.admin.authorization_management import create_permission, create_resource, list_permissions, list_policies, list_resources, simulate_policy
from app.models import realm
from app.models.authorization import PermissionCreate, PolicyCreate, ResourceCreate
from app.models.client import ClientCreate, ClientUpdate
from app.models.role import RoleMappingRequest
from app.models.user import PasswordReset, UserCreate, UserUpdate
from app.admin import role_management
from app.admin import groupe_management
from app.admin.admin_master import keycloak_master_request

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/users")
def create_user(user: UserCreate):
    return user_management.create_user(
        username=user.username,
        email=user.email,
        first_name=user.first_name if user.first_name is not None else "",
        last_name=user.last_name if user.last_name is not None else ""
    )

@router.get("/users")
def list_users():
    return user_management.list_users()

@router.get("/users/{user_id}")
def get_user(user_id: str):
    return user_management.get_user_by_id(user_id)

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    return user_management.delete_user(user_id)

def send_verify_email(user_id):
    return keycloak_admin_request("PUT", f"users/{user_id}/send-verify-email")

@router.put("/users/{user_id}")
def update_user_endpoint(user_id: str, user: UserUpdate):
    return user_management.update_user(
        user_id,
        email=user.email,
        first_name=user.first_name if user.first_name is not None else "",
        last_name=user.last_name if user.last_name is not None else ""
    )

@router.put("/users/{user_id}/reset-password")
def reset_password_endpoint(user_id: str, payload: PasswordReset):
    return user_management.reset_password(user_id, payload.password)

# Gestion des roles--------------------------------------------------------------
# CRUD ROLES REALM

@router.post("/roles")
def create_role_endpoint(role_data: dict):
    return role_management.create_role(role_data)

@router.get("/roles")
def list_roles_endpoint():
    return role_management.list_roles()

@router.put("/roles/{role_name}")
def update_role_endpoint(role_name: str, role_data: dict):
    return role_management.update_role(role_name, role_data)

@router.delete("/roles/{role_name}")
def delete_role_endpoint(role_name: str):
    return role_management.delete_role(role_name)


# Attribution de rôles
@router.post("/users/{user_id}/roles")
def assign_role(user_id: str, roles: list[str]):
    """
    Assigne plusieurs rôles à un utilisateur.
    Ex body JSON: ["admin", "etudiant"]
    """
    return role_management.assign_roles_to_user(user_id, roles)


# Suppression de rôles
@router.delete("/users/{user_id}/roles")
def remove_role(user_id: str, roles: list[str]):
    """
    Retire plusieurs rôles à un utilisateur.
    Ex body JSON: ["admin", "etudiant"]
    """
    return role_management.remove_roles_from_user(user_id, roles)

@router.get("/users/{user_id}/role-mappings")
def get_user_role_mappings(user_id: str):
    """
    Retourne les mappings de rôles Realm et Client d'un utilisateur.
    """
    return role_management.get_role_mappings(user_id)

@router.post("/users/{user_id}/role-mappings")
def modify_role_mappings(user_id: str, data: RoleMappingRequest):
    return role_management.update_role_mappings(
        user_id,
        data.scope,
        data.roles,
        data.action
    )

# CRUD ROLES CLIENT
@router.post("/clients/{client_id}/roles")
def create_client_role_endpoint(client_id: str, role_data: dict):
    return role_management.create_client_role(client_id, role_data)

@router.get("/clients/{client_id}/roles")
def list_client_roles_endpoint(client_id: str):
    return role_management.list_client_roles(client_id)

@router.put("/clients/{client_id}/roles/{role_name}")
def update_client_role_endpoint(client_id: str, role_name: str, role_data: dict):
    return role_management.update_client_role(client_id, role_name, role_data)

@router.delete("/clients/{client_id}/roles/{role_name}")
def delete_client_role_endpoint(client_id: str, role_name: str):
    return role_management.delete_client_role(client_id, role_name)

# Attribution de rôles client
@router.post("/users/{user_id}/clients/{client_id}/roles")
def assign_client_role(user_id: str, client_id: str, roles: list[str]):
    """
    Assigne plusieurs rôles client à un utilisateur.
    Ex body JSON: ["client_role_1", "client_role_2"]
    """
    return role_management.assign_client_roles_to_user(user_id, client_id, roles)


# Suppression de rôles client
@router.delete("/users/{user_id}/clients/{client_id}/roles")
def remove_client_role(user_id: str, client_id: str, roles: list[str]):
    """
    Retire plusieurs rôles client à un utilisateur.
    Ex body JSON: ["client_role_1"]
    """
    return role_management.remove_client_roles_from_user(user_id, client_id, roles)


# Gestion des groupes---------------------------------------------------------

# Création d’un groupe
@router.post("/groups")
def create_group_endpoint(group_data: dict):
    return groupe_management.create_group(group_data)

# Consultation des groupes
@router.get("/groups")
def list_groups_endpoint():
    return groupe_management.list_groups()

# Mise à jour d’un groupe
@router.put("/groups/{group_id}")
def update_group_endpoint(group_id: str, group_data: dict):
    return groupe_management.update_group(group_id, group_data)

# Suppression d’un groupe
@router.delete("/groups/{group_id}")
def delete_group_endpoint(group_id: str):
    return groupe_management.delete_group(group_id)

@router.put("/groups/{group_id}/users/{user_id}")
def add_user_to_group_endpoint(group_id: str, user_id: str):
    # On appelle la fonction qui construit la bonne URL Keycloak /users/{userId}/groups/{groupId}
    return groupe_management.add_user_to_group(user_id, group_id)

@router.delete("/groups/{group_id}/users/{user_id}")
def remove_user_from_group_endpoint(group_id: str, user_id: str):
    return groupe_management.remove_user_from_group(user_id, group_id)


# Gestion des clients---------------------------------------------------

@router.post("/clients")
def create_client(client: ClientCreate):
    """
    Créer un nouveau client dans Keycloak
    """
    try:
        data = {
            "clientId": client.clientId,
            "enabled": True,
            "redirectUris": client.redirectUris,
            "publicClient": client.publicClient,
            "protocol": "openid-connect",
            "directAccessGrantsEnabled": True
        }

        # Si le client n’est pas public → il faut un secret
        if not client.publicClient:
            data["secret"] = client.secret or "defaultSecret"

        return keycloak_admin_request("POST", "clients", json=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/clients")
def list_clients(
    client_id: Optional[str] = Query(None, description="Filtrer par clientId exact"),
    search: Optional[str] = Query(None, description="Recherche partielle dans clientId"),
    enabled: Optional[bool] = Query(None, description="Filtrer selon l'état (activé ou non)"),
):
    """
    Liste les clients Keycloak avec options de recherche et filtrage
    """
    try:
        clients = keycloak_admin_request("GET", "clients")
        if clients is None:
            clients = []

        # Filtrage par clientId exact
        if client_id:
            clients = [c for c in clients if c.get("clientId") == client_id]

        # Recherche partielle dans clientId
        if search:
            clients = [c for c in clients if search.lower() in c.get("clientId", "").lower()]

        # Filtrage par statut enabled
        if enabled is not None:
            clients = [c for c in clients if c.get("enabled") == enabled]

        return {"count": len(clients), "results": clients}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/clients/{client_id}")
def update_client(client_id: str, client: ClientUpdate):
    try:
        data = client.dict(exclude_unset=True)  # ✅ n’inclut que les champs envoyés
        if not data:
            raise HTTPException(status_code=400, detail="Aucune donnée fournie pour la mise à jour")

        return keycloak_admin_request("PUT", f"clients/{client_id}", json=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clients/{client_id}")
def delete_client_endpoint(client_id: str):
    return client_management.delete_client(client_id)


# Gestion des Sessions---------------------------------------------------

@router.get("/users/{user_id}/sessions")
def get_user_sessions(user_id: str):
    """
    Récupère les sessions actives d’un utilisateur
    """
    try:
        endpoint = f"users/{user_id}/sessions"
        sessions = keycloak_admin_request("GET", endpoint)
        if sessions is None:
            sessions = []

        formatted = []
        for s in sessions:
            formatted.append({
                "id": s.get("id"),
                "ipAddress": s.get("ipAddress"),
                "start": s.get("start"),  # timestamp
                "lastAccess": s.get("lastAccess"),
                "clients": list(s.get("clients", {}).keys()),  # apps utilisées
            })

        return {"count": len(formatted), "sessions": formatted}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/{user_id}/logout")
def force_logout(user_id: str):
    """
    Déconnexion forcée d’un utilisateur (toutes ses sessions sont invalidées)
    """
    try:
        endpoint = f"users/{user_id}/logout"
        keycloak_admin_request("POST", endpoint)
        return {"message": f"Utilisateur {user_id} déconnecté avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/users/{user_id}/offline-sessions/{client_id}")
def get_offline_sessions(user_id: str, client_id: str):
    """
    Récupère les sessions offline d’un utilisateur pour un client donné
    """
    try:
        endpoint = f"users/{user_id}/offline-sessions/{client_id}"
        sessions = keycloak_admin_request("GET", endpoint)
        if sessions is None:
            sessions = []
        return {"count": len(sessions), "sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Gestion des Identites Federees---------------------------------------------

@router.post("/users/{user_id}/federated-identity/{provider}")
def add_federated_identity(user_id: str, provider: str, payload: dict):
    """
    Lie un compte utilisateur à une identité fédérée (Google, Facebook, etc.)
    """
    try:
        endpoint = f"users/{user_id}/federated-identity/{provider}"
        body = {
            "userId": payload.get("userId"),
            "userName": payload.get("userName")
        }
        # IMPORTANT : envoyer en JSON
        response = keycloak_admin_request("POST", endpoint, json=body)
        return {"message": f"Identité {provider} liée avec succès", "details": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/federated-identity")
def list_federated_identities(user_id: str):
    """
    Liste toutes les identités fédérées liées à un utilisateur.
    """
    try:
        endpoint = f"users/{user_id}/federated-identity"
        response = keycloak_admin_request("GET", endpoint)
        if response is None:
            response = []
        return {"count": len(response), "federated_identities": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}/federated-identity/{provider}")
def remove_federated_identity(user_id: str, provider: str):
    """
    Supprime une identité fédérée liée à un utilisateur
    """
    try:
        endpoint = f"users/{user_id}/federated-identity/{provider}"
        keycloak_admin_request("DELETE", endpoint)
        return {"message": f"Identité {provider} supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Gestion des Politiques d’Autorisation---------------------------------------

# Resources
@router.post("/clients/{client_id}/resources")
def add_resource(client_id: str, resource: ResourceCreate):
    return create_resource(client_id, resource.dict())

@router.get("/clients/{client_id}/resources")
def get_resources(client_id: str):
    return list_resources(client_id)

# Policies
@router.post("/clients/{client_id}/policies")
def create_policy(client_id: str, policy: PolicyCreate):
    endpoint = f"clients/{client_id}/authz/resource-server/policy/{policy.type}"
    
    body = policy.dict(exclude_unset=True)  # exclut les champs non définis
    return keycloak_admin_request("POST", endpoint, json=body)


@router.get("/clients/{client_id}/policies")
def get_policies(client_id: str):
    return list_policies(client_id)

# Permissions
@router.post("/clients/{client_id}/permissions")
def add_permission(client_id: str, permission: PermissionCreate):
    return create_permission(client_id, permission.dict())

@router.get("/clients/{client_id}/permissions")
def get_permissions(client_id: str):
    return list_permissions(client_id)

# Simulation
@router.post("/clients/{client_id}/simulate")
def simulate_authorization(client_id: str, payload: dict):
    """
    Simule l'application des politiques d'autorisation pour un utilisateur donné.
    """
    return simulate_policy(client_id, payload)


# Audit et Journalisation

@router.get("/logs")
def get_logs(
    event_type: Optional[str] = None,
    user: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """
    Récupère les logs d'événements du realm administré avec filtres :
    - type : type d'événement
    - user : id de l'utilisateur
    - from_date / to_date : intervalle de date au format 'YYYY-MM-DDTHH:MM:SS'
    """
    try:
        return list_events(event_type, user, from_date, to_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Export des logs au format CSV

@router.get("/logs/export")
def export_logs(
    event_type: Optional[str] = None,
    user: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """
    Exporte les logs filtrés en CSV.
    """
    return export_events_csv(event_type, user, from_date, to_date)


# Gestion des Realms------------------------------------------------------------
@router.post("/realms")
def create_new_realm(data: realm.RealmCreateRequest):
    try:
        result = admin_realm.create_realm(data)
        return {"message": f"Realm '{data.realm_name}' créé avec succès", "details": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/realms/{realm_name}")
def configure_realm(realm_name: str, data: realm.RealmUpdateRequest):
    try:
        result = admin_realm.update_realm(realm_name, data)
        return {"message": f"Realm '{realm_name}' mis à jour avec succès", "details": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/realms/{realm_name}")
def remove_realm(realm_name: str):
    try:
        admin_realm.delete_realm(realm_name)
        return {"message": f"Realm '{realm_name}' supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


