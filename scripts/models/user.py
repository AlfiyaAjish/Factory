from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    user_id: str
    username: str
    role: str      # "admin", "engineer", "operator"
    password: str

class UserLogin(BaseModel):
    user_id: str
    password: str

class OwnershipAssign(BaseModel):
    user_id: str
    role: str
    line: Optional[str] = None
    machine_id: Optional[str] = None

class AdminRegister(BaseModel):
    user_id: str
    username: str
    password: str
    secret_key: str

class UpdatePasswordRequest(BaseModel):
    user_id: str
    old_password: str
    new_password: str
