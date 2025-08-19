from app.admin.admin_client import keycloak_admin_request


# Ressources
def create_resource(client_id: str, resource: dict):
    endpoint = f"clients/{client_id}/authz/resource-server/resource"
    return keycloak_admin_request("POST", endpoint, json=resource)

def list_resources(client_id: str):
    endpoint = f"clients/{client_id}/authz/resource-server/resource"
    return keycloak_admin_request("GET", endpoint)

# Policies
def create_policy(client_id: str, policy: dict):
    endpoint = f"clients/{client_id}/authz/resource-server/policy/{policy['type']}"
    
    # Supprimer config si présent pour user/role policies
    if policy["type"] in ["user", "role"] and "config" in policy:
        policy.pop("config")
    
    return keycloak_admin_request("POST", endpoint, json=policy)



def list_policies(client_id: str):
    endpoint = f"clients/{client_id}/authz/resource-server/policy"
    return keycloak_admin_request("GET", endpoint)

# Permissions
def create_permission(client_id: str, permission: dict):
    endpoint = f"clients/{client_id}/authz/resource-server/permission/resource"
    return keycloak_admin_request("POST", endpoint, json=permission)

def list_permissions(client_id: str):
    endpoint = f"clients/{client_id}/authz/resource-server/permission/resource"
    return keycloak_admin_request("GET", endpoint)



