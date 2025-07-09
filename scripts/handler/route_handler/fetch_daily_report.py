from fastapi import APIRouter, Query
# from pymongo import MongoClient
# import os
from typing import Optional,List,Dict
from scripts.utils.mongodb_utils import reports_collection

router = APIRouter()
# client = MongoClient(os.getenv("MONGO_URI"))
# db = client["smart_factory"]
# metrics_collection = db["metrics"]
# reports_collection = db["reports"]

# @router.get("/")
# def get_daily_report(
#     date: str = Query(..., description="Format: YYYY-MM-DD"),
#     machine_id: Optional[str] = Query(None)
# ):
#     query = {
#         "type": "daily",
#         "date": date
#     }
#
#     if machine_id:
#         query["machine_id"] = machine_id
#
#     reports = list(reports_collection.find(query, {"_id": 0}))
#
#
#     if not reports:
#         return {"message": "No report data found for given date/machine."}
#
#     return reports

def fetch_daily_reports(date: str, machine_id: Optional[str] = None) -> List[Dict]:
    query = {
        "type": "daily",
        "date": date
    }

    if machine_id:
        query["machine_id"] = machine_id

    reports = list(reports_collection.find(query, {"_id": 0}))
    return reports