# from fastapi import APIRouter, Query
from datetime import datetime
from scripts.utils.mongodb_utils import reports_collection



# @router.get("/")
# def get_monthly_report(start_date: str = Query(...), end_date: str = Query(...), machine_id: str = Query(...)):
#
#     # date_start = f"{start_date}T00:00:00"
#     # date_end = f"{end_date}T23:59:59"
#
#     query = {
#         "date": {"$gte": start_date, "$lte": end_date},
#         "machine_id": machine_id
#     }
#
#
#     reports = list(reports_collection.find(query))
#     print(reports)
#
#     if not reports:
#         return {"message": "No data found"}
#
#     total_units = sum(d.get("units_produced", 0) for d in reports)
#     temp_sum = sum(d.get("avg_temperature", 0) for d in reports)
#     count = len(reports)
#     avg_temp = round(temp_sum / count, 2) if count > 0 else 0
#     line = reports[0].get("line", "unknown")
#     alert_count=sum(d.get("total_alerts", 0) for d in reports)
#
#     total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
#     total_hours = total_days * 24
#     efficiency = round(total_units / total_hours, 2) if total_hours > 0 else 0
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


def get_monthly_reports(start_date: str , end_date: str , machine_id: str):
    # date_start = f"{start_date}T00:00:00"
    # date_end = f"{end_date}T23:59:59"

    query = {
        "type":"daily",
        "date": {"$gte": start_date, "$lte": end_date},
        "machine_id":machine_id
    }

    reports = list(reports_collection.find(query))
    if not reports:
        return None
    total_units = sum(d.get("total_units", 0) for d in reports)
    temp_sum = sum(d.get("avg_temperature", 0) for d in reports)
    count = len(reports)
    avg_temp = round(temp_sum / count, 2) if count > 0 else 0
    line = reports[0].get("line", "unknown")
    alert_count = sum(d.get("total_alerts", 0) for d in reports)

    total_days = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days + 1
    total_hours = total_days * 24
    efficiency = round(total_units / total_hours, 2) if total_hours > 0 else 0
    print(efficiency)

    return {
        "machine_id": machine_id,
        "line": line,
        "start_date": start_date,
        "end_date": end_date,
        "total_units": total_units,
        "avg_temperature": avg_temp,
        "alerts": alert_count,
        "efficiency": efficiency
    }