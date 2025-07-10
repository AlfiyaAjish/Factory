from fastapi import APIRouter, HTTPException,Query,Depends
from scripts.utils.mongodb_utils import register_machine, is_machine_registered
from scripts.models.models import Machine
from scripts.handler.route_handler import fetch_daily_report, fetch_monthwise_report, list_machines
from typing import Optional
from scripts.handler.route_handler.jwt_handler import get_current_user
from scripts.utils.mongodb_utils import machines_collection

router = APIRouter()

@router.post("/machine/register")
def register(machine: Machine):
    if is_machine_registered(machine.machine_id):
        raise HTTPException(status_code=409, detail="Machine already registered")

    register_machine(machine.dict())
    return {"message": " Machine registered successfully"}




@router.get("/report/daily")
def get_daily_report(
    date: str = Query(..., description="Format: YYYY-MM-DD"),
    machine_id: Optional[str] = Query(None),
    user: dict = Depends(get_current_user)
):
    role = user["role"]
    owned_by = user["owned_by"]

    machine_doc = machines_collection.find_one({"machine_id": machine_id})
    if not machine_doc:
        raise HTTPException(status_code=404, detail="Machine not found")


    if role == "operator":
        if not machine_id:
            machine_id = owned_by
        elif machine_id != owned_by:
            raise HTTPException(status_code=403, detail=" Access denied: Not your machine.")
    elif role == "engineer":
        if not machine_id:
            raise HTTPException(status_code=403, detail=" Machine ID required for engineers.")
        elif machine_doc.get("line") != owned_by:
            raise HTTPException(status_code=403, detail="Access denied: Not your line")


    reports = fetch_daily_report.fetch_daily_reports(date, machine_id)

    if not reports:
        return {"message": "No report data found for given date/machine."}

    return reports


@router.get("/report/monthly")
def get_monthly_report(
    start_date: str = Query(..., description="Format: YYYY-MM-DD"),
    end_date: str = Query(..., description="Format: YYYY-MM-DD"),
    machine_id: str = Query(..., description="Machine ID"),
    user: dict = Depends(get_current_user)
):

    role = user["role"]
    owned_by = user["owned_by"]

    machine_doc = machines_collection.find_one({"machine_id": machine_id})
    if not machine_doc:
        raise HTTPException(status_code=404, detail="Machine not found")

    if role == "operator":
        if not machine_id:
            machine_id = owned_by
        elif machine_id != owned_by:
            raise HTTPException(status_code=403, detail=" Access denied: Not your machine.")
    elif role == "engineer":
        if not machine_id:
            raise HTTPException(status_code=403, detail=" Machine ID required for engineers.")
        elif machine_doc.get("line") != owned_by:
            raise HTTPException(status_code=403, detail="Access denied: Not your line")
    reports = fetch_monthwise_report.get_monthly_reports(start_date, end_date, machine_id)

    if not reports:
        return {"message": "No data found"}

    return reports

@router.get("/machines")
def list_all_machines():

    machines= list_machines.get_all_machines()
    if not machines:
        return{"message":"No machines found"}
    return machines