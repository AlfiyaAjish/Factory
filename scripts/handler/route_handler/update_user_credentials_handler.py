import hashlib
from fastapi import HTTPException
from scripts.utils.mongodb_utils import users_collection

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def update_user_password(user_id: str, old_password: str, new_password: str):
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if hash_password(old_password) != user["password"]:
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    new_hashed = hash_password(new_password)
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"password": new_hashed}}
    )
    return {"message": "Password updated successfully"}
