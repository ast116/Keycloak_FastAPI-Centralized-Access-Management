from pydantic import BaseModel
from typing import List, Dict, Optional

# Resource
class ResourceCreate(BaseModel):
    name: str
    uris: List[str]
    scopes: List[Dict[str, str]]  # [{"name": "read"}, {"name": "write"}]

# Policy
class PolicyCreate(BaseModel):
    name: str
    type: str               # "user", "role", "js", "rule", etc.
    logic: str              # "POSITIVE" ou "NEGATIVE"
    decisionStrategy: str   # "AFFIRMATIVE" ou "UNANIMOUS"
    users: Optional[List[str]] = None   # uniquement pour type "user"
    roles: Optional[List[Dict]] = None  # uniquement pour type "role"
    config: Optional[Dict] = None       # optionnel, pour type "js" ou "rule"

# Permission
class PermissionCreate(BaseModel):
    name: str
    resources: List[str]
    scopes: List[str]
    policies: List[str]


