from pydantic import BaseModel

class UserRegister(BaseModel):
    user_id: str
    username: str
    role: str      # "admin", "engineer", "operator"
    owned_by: str
    password: str

class UserLogin(BaseModel):
    user_id: str
    password: str
