from fastapi import APIRouter
from pydantic import BaseModel
from scripts.handler.celery.periodic_tasks import generate_daily_report,run_daily_chain_task

router = APIRouter()

class MonthRange(BaseModel):
    start_date: str
    end_date: str

# @router.post("/daily")
# def trigger_daily_report():
#     task = generate_daily_report.delay()
#     return {"message": "Daily report task triggered", "task_id": task.id}

@router.post("/daily/chain")
def trigger_daily_report():
    task=run_daily_chain_task.delay()
    return {"message": "Daily report task triggered", "task_id": task.id}

# @router.post("/monthly")
# def trigger_monthly_report(payload: MonthRange):
#     task = generate_monthly_report.delay(payload.start_date, payload.end_date)
#     return {"message": " Monthly report task triggered", "task_id": task.id}
