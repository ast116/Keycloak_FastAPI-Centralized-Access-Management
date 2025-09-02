from pydantic import BaseModel
from typing import Optional, Dict

class IdentityProviderCreateRequest(BaseModel):
    alias: str
    provider_id: str  # ex: "google", "facebook", "github"
    enabled: bool = True
    trust_email: bool = True
    store_token: bool = False
    link_only: bool = False
    config: Dict[str, str]  # ex: clientId, clientSecret, authorizationUrl...

class IdentityProviderUpdateRequest(BaseModel):
    enabled: Optional[bool] = None
    trust_email: Optional[bool] = None
    store_token: Optional[bool] = None
    link_only: Optional[bool] = None
    config: Optional[Dict[str, str]] = None

class IdentityProviderDeleteRequest(BaseModel):
    alias: str
