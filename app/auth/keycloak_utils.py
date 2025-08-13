import requests
from jose import jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode 
from jose import jwk
from app import config

# Récupérer les clés publiques de Keycloak
def get_public_keys():
    jwks = requests.get(config.KEYCLOAK_OPENID_CONFIG_URL).json()
    return {key["kid"]: key for key in jwks["keys"]}

# Valider le token JWT
def verify_token(token: str):
    try:
        jwks = get_public_keys()
        headers = jwt.get_unverified_header(token)
        key_data = jwks.get(headers["kid"])

        if not key_data:
            raise Exception("Clé publique non trouvée pour ce token")

        # Convertir la clé JWK en objet utilisable
        public_key = jwk.construct(key_data)

        # Décoder le token (A remettre plus tard a cause de aud)
        payload = jwt.decode(
            token,
            public_key.to_pem().decode("utf-8"),
            algorithms=[key_data["alg"]],
            options={"verify_aud": False}  # Ignore l'audience
        )

        return payload

    except JWTError as e:
        raise Exception(f"Token invalide : {str(e)}")
