from pydantic import BaseModel
from typing import Optional

class RealmCreateRequest(BaseModel):
    realm_name: str
    display_name: Optional[str] = None
    enabled: bool = True
    ssl_required: str = "external"  # none, external, all
    registration_allowed: bool = False
    login_with_email_allowed: bool = True
    password_policy: Optional[str] = None  # ex: "length(8) and digits(1)"
    brute_force_protected: bool = False

class RealmUpdateRequest(BaseModel):
    enabled: Optional[bool] = None
    display_name: Optional[str] = None
    ssl_required: Optional[str] = None  # none, external, all
    registration_allowed: Optional[bool] = None
    login_with_email_allowed: Optional[bool] = None
    password_policy: Optional[str] = None
    brute_force_protected: Optional[bool] = None
