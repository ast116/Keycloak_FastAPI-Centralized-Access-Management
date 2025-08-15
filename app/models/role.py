from pydantic import BaseModel
from typing import Optional
from typing import List, Dict

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleOut(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = None

class RoleMappingRequest(BaseModel):
    scope: str               # "realm" ou nom du client (ex: "my-client")
    action: str              # "add" ou "remove"
    roles: List[Dict[str, str]]  # [{"name": "role_name"}]
