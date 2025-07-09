# from fastapi import APIRouter, HTTPException
# from scripts.utils.mongodb_utils import register_machine, is_machine_registered
# from scripts.models.models import Machine
# router = APIRouter()
#
# @router.post("/")
# def register(machine: Machine):
#     if is_machine_registered(machine.machine_id):
#         raise HTTPException(status_code=409, detail="Machine already registered")
#
#     register_machine(machine.dict())
#     return {"message": " Machine registered successfully"}
