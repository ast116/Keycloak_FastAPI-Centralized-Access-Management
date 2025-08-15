from fastapi import APIRouter, Depends
from app.admin import user_management
from app.admin.admin_client import keycloak_admin_request
from app.models.role import RoleMappingRequest
from app.models.user import PasswordReset, UserCreate, UserUpdate
from app.admin import role_management
from app.admin import groupe_management

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

