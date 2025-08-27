import os
# =======================
# Phase 1 - Client Gateway
# =======================

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "Final-project")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-gateway")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "g2fvDMdeeRla71CNw6TpWQB9o1TnT8AO")  # à remplacer

# URL complète pour introspection ou récupération de clés
KEYCLOAK_OPENID_CONFIG_URL = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"


# =======================
# Phase 2 - Client Admin
# =======================
KEYCLOAK_ADMIN_CLIENT_ID = os.getenv("KEYCLOAK_ADMIN_CLIENT_ID", "fastapi-admin")
KEYCLOAK_ADMIN_CLIENT_SECRET = os.getenv(
    "KEYCLOAK_ADMIN_CLIENT_SECRET",
    "DwYODdMaoYLtfIgAf001PMIWWh7nixsk"  #  Mon client secret pour fastapi-admin
)

# URL pour obtenir un token admin
KEYCLOAK_ADMIN_TOKEN_URL = (
    f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
)

# URL racine de l’API Admin
KEYCLOAK_ADMIN_BASE_URL = (
    f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}"
)

# Pour la gestion globale des realms
KEYCLOAK_ADMIN_GLOBAL_URL = f"{KEYCLOAK_SERVER_URL}/admin/realms"




