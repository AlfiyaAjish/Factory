# from fastapi import APIRouter, Query
from datetime import datetime
from scripts.utils.mongodb_utils import reports_collection





# def get_monthly_reports(start_date: str , end_date: str , machine_id: str):
#     # date_start = f"{start_date}T00:00:00"
#     # date_end = f"{end_date}T23:59:59"
#
#     query = {
#         "type":"daily",
#         "date": {"$gte": start_date, "$lte": end_date},
#         "machine_id":machine_id
#     }
#
#     reports = list(reports_collection.find(query))
#     if not reports:
#         return None
#     total_units = sum(d.get("total_units", 0) for d in reports)
#     temp_sum = sum(d.get("avg_temperature", 0) for d in reports)
#     count = len(reports)
#     avg_temp = round(temp_sum / count, 2) if count > 0 else 0
#     line = reports[0].get("line", "unknown")
#     alert_count = sum(d.get("total_alerts", 0) for d in reports)
#
#     total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
#     total_hours = total_days * 24
#     efficiency = round(total_units / total_hours, 2) if total_hours > 0 else 0
#     print(efficiency)
#
#     return {
#         "machine_id": machine_id,
#         "line": line,
#         "start_date": start_date,
#         "end_date": end_date,
#         "total_units": total_units,
#         "avg_temperature": avg_temp,
#         "alerts": alert_count,
#         "efficiency": efficiency
#     }


from datetime import datetime
from scripts.utils.mongodb_utils import reports_collection
from scripts.utils.mongodb_utils import clean_mongo_id

def get_monthly_reports(start_date: str, end_date: str, machine_id: str):
    query = {
        "type": "daily",
        "date": {"$gte": start_date, "$lte": end_date},
        "machine_id": machine_id
    }

    reports = list(reports_collection.find(query))
    if not reports:
        return None


    reports = [clean_mongo_id(r) for r in reports]


    total_units = sum(d.get("total_units", 0) for d in reports)
    temp_sum = sum(d.get("avg_temperature", 0) for d in reports)
    alert_count = sum(d.get("total_alerts", 0) for d in reports)
    count = len(reports)

    avg_temp = round(temp_sum / count, 2) if count > 0 else 0
    line = reports[0].get("line", "unknown")

    total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
    total_hours = total_days * 24
    efficiency = round(total_units / total_hours, 2) if total_hours > 0 else 0


    sorted_daily_reports = sorted(reports, key=lambda x: x["date"])


    return {
        "summary": {
            "machine_id": machine_id,
            "line": line,
            "start_date": start_date,
            "end_date": end_date,
            "total_units": total_units,
            "avg_temperature": avg_temp,
            "alerts": alert_count,
            "efficiency": efficiency
        },
        "daily_reports": sorted_daily_reports
    }
