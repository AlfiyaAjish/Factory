# from fastapi import APIRouter, Query
# from pymongo import MongoClient
# import os
from typing import Optional,List,Dict
from scripts.utils.mongodb_utils import reports_collection



def fetch_daily_reports(date: str, machine_id: Optional[str] = None) -> List[Dict]:
    query = {
        "type": "daily",
        "date": date
    }

    if machine_id:
        query["machine_id"] = machine_id

    reports = list(reports_collection.find(query, {"_id": 0}))
    return reports