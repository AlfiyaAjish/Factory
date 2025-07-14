from fastapi import HTTPException
from scripts.utils.mongodb_utils import users_collection, ownership_collection
from scripts.models.user import OwnershipAssign

def handle_assign_ownership(payload: OwnershipAssign, current_user: dict):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can assign ownership")

    user = users_collection.find_one({"user_id": payload.user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ownership_data = {"user_id": payload.user_id, "role": payload.role}

    if payload.role == "engineer":
        ownership_data["line"] = payload.line
    elif payload.role == "operator":
        ownership_data["machine_id"] = payload.machine_id
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    ownership_collection.update_one(
        {"user_id": payload.user_id},
        {"$set": ownership_data},
        upsert=True
    )

    return {"message": "Ownership assigned/updated"}
