from fastapi import APIRouter, HTTPException
from scripts.models.user import UserRegister, UserLogin
from scripts.handler.route_handler.jwt_handler import create_jwt
from scripts.utils.mongodb_utils import users_collection
import hashlib

router = APIRouter()


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register")
def register_user(user: UserRegister):
    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=409, detail="User already exists")

    hashed = hash_password(user.password)
    users_collection.insert_one({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "owned_by": user.owned_by,
        "password": hashed
    })
    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"user_id": user.user_id})
    if not db_user or hash_password(user.password) != db_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(db_user["user_id"], db_user["role"], db_user["owned_by"])
    return {"access_token": token}
