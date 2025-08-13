# app/routers/admin_routes.py

from fastapi import APIRouter
from app.admin import user_management
from app.admin.admin_client import keycloak_admin_request
from app.models.user import PasswordReset, UserCreate, UserUpdate

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

