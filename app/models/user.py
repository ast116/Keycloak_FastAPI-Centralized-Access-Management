from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    roles: List[str] = []
   
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""

class PasswordReset(BaseModel):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
