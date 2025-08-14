from fastapi import APIRouter, Depends
from app.admin import user_management
from app.admin.admin_client import keycloak_admin_request
from app.models.user import PasswordReset, UserCreate, UserUpdate
from app.admin import role_management

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