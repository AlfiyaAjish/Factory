
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

from celery import chain
from scripts.utils.celery.celery import celery_app


from scripts.utils.mongodb_utils import alerts_collection,reports_collection,metrics_collection



load_dotenv()


# client = MongoClient(os.getenv("MONGO_URI"))
# db = client["smart_factory"]
# metrics_collection = db["metrics"]
# reports_collection = db["reports"]
# alerts_collection= db["alerts"]



@celery_app.task(name="generate_daily_report", bind=True, max_retries=3, default_retry_delay=60)
def generate_daily_report(self):
    try:
        today = datetime.utcnow().strftime('%Y-%m-%d')
        start_time = f"{today}T00:00:00"
        end_time = f"{today}T23:59:59"

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_time, "$lte": end_time}}},
            {"$group": {
                "_id": "$machine_id",
                "total_units": {"$sum": "$units_produced"},
                "avg_temperature": {"$avg": "$temperature"},
                "line": {"$first": "$line"}
            }}
        ]

        results = list(metrics_collection.aggregate(pipeline))
        daily_data = []

        for item in results:
            machine_id = item["_id"]
            total_alerts = alerts_collection.count_documents({
                "machine_id": machine_id,
                "timestamp": {"$gte": start_time, "$lte": end_time}
            })

            daily_data.append({
                "machine_id": machine_id,
                "line": item.get("line", "unknown"),
                "total_units": item["total_units"],
                "avg_temperature": round(item["avg_temperature"], 2)
                    if item["avg_temperature"] is not None else 0.0,
                "total_alerts": total_alerts,
                "date": today,
                "generated_at": datetime.utcnow().isoformat(),
                "type": "daily"
            })

        return daily_data

    except Exception as e:
        raise self.retry(exc=e)

@celery_app.task(name="compute_efficiency_analysis")
def compute_efficiency_analysis(reports: list):
    for report in reports:
        report["efficiency"] = round(report["total_units"] / 24.0, 2)
    return reports

@celery_app.task(name="store_daily_summary")
def store_daily_summary(reports: list):
    count = 0
    for report in reports:
        reports_collection.update_one(
            {
                "type": "daily",
                "date": report["date"],
                "machine_id": report["machine_id"]
            },
            {"$set": report},
            upsert=True
        )
        count += 1

    return {"message": "Daily summaries stored", "count": count}

@celery_app.task(name="run_daily_chain_task")
def run_daily_chain_task():
    print("run_daily_chain_task triggered")
    chain(
        generate_daily_report.s(),
        compute_efficiency_analysis.s(),
        store_daily_summary.s()
    )()





