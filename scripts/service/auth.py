from fastapi import APIRouter, HTTPException,Depends
from scripts.models.user import UserRegister, UserLogin,AdminRegister,UpdatePasswordRequest
from scripts.handler.route_handler.update_user_credentials_handler import update_user_password
from scripts.handler.route_handler.jwt_handler import create_jwt,get_current_user
from scripts.utils.mongodb_utils import users_collection,ownership_collection
import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()





# admin registration

@router.post("/register-admin")
def register_admin(payload: AdminRegister):
    expected_secret = os.getenv("ADMIN_SECRET_KEY")

    if payload.secret_key != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid admin secret key")

    if users_collection.find_one({"user_id": payload.user_id}):
        raise HTTPException(status_code=409, detail="Admin user already exists")

    users_collection.insert_one({
        "user_id": payload.user_id,
        "username": payload.username,
        "role": "admin",
        "owned_by": None,
        "password": hash_password(payload.password)
    })

    return {"message": "Admin registered successfully"}


#user registration

@router.post("/register")
def register_user(user: UserRegister, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can register users")

    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=409, detail="User already exists")

    hashed = hash_password(user.password)
    users_collection.insert_one({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "password": hashed
    })
    return {"message": "User registered successfully"}




#user login



@router.post("/login")
def login_user(user: UserLogin):
    db_user = users_collection.find_one({"user_id": user.user_id})
    if not db_user or hash_password(user.password) != db_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = db_user["role"]
    ownership = ownership_collection.find_one({"user_id": user.user_id})
    print("Ownership:", ownership)

    owned_by = None
    if ownership:
        if role == "engineer":
            owned_by = ownership.get("line")
        elif role == "operator":
            owned_by = ownership.get("machine_id")
        else:
            owned_by = None

    print("Owned By:", owned_by)
    token = create_jwt(db_user["user_id"], role, owned_by)
    return {"access_token": token}


# update user password

@router.post("/update-password")
def update_password(payload: UpdatePasswordRequest, current_user: dict = Depends(get_current_user)):
    if current_user["sub"] != payload.user_id:
        raise HTTPException(status_code=403, detail="You can only update your own password")

    return update_user_password(
        user_id=payload.user_id,
        old_password=payload.old_password,
        new_password=payload.new_password
    )
