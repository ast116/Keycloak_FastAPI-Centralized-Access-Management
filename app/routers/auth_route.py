
from fastapi import APIRouter, Form, HTTPException
import requests
from app import config

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token", include_in_schema=False)  # 👈 cache cette route dans Swagger UI
def get_token_from_keycloak(
    username: str = Form(...),
    password: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
):
    data = {
        "grant_type": "password",  # 👈 obligatoire pour Keycloak
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
    }

    response = requests.post(
        f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}/protocol/openid-connect/token",
        data=data
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()