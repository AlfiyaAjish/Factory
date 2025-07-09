from pydantic import BaseModel
from typing import Optional

class ReportModel(BaseModel):
    machine_id: str
    line: str
    total_units: int
    avg_temperature: float
    total_alerts: int
    generated_at: str
    type: str
    date: str
    efficiency: float

class Machine(BaseModel):
    machine_id: str
    line: str
    location: str
    operator: str