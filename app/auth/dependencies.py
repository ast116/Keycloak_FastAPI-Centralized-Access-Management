from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.keycloak_utils import verify_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = verify_token(token)
        username = payload.get("preferred_username")
        email = payload.get("email")
        roles = payload.get("realm_access", {}).get("roles", [])

        if username is None:
            raise HTTPException(status_code=401, detail="Utilisateur non valide")

        return User(username=username, email=email, roles=roles)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
