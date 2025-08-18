from typing import List, Optional
from pydantic import BaseModel


# Modele de validation pour la création
class ClientCreate(BaseModel):
    clientId: str
    redirectUris: list[str] = []
    publicClient: bool = False
    secret: str | None = None
    enabled: bool | None = None


# Pour la mise à jour
class ClientUpdate(BaseModel):
    redirectUris: Optional[List[str]] = None
    publicClient: Optional[bool] = None
    secret: Optional[str] = None
    enabled: Optional[bool] = None