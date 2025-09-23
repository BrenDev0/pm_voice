from typing_extensions import TypedDict
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional

class InvestmentData(BaseModel):
    type: str
    location: str
    budget: float
    action: str

class ClientData(BaseModel):
    name: str
    email: str
    phone: str

class AppointmentData(BaseModel):
    datatime: datetime

class State(TypedDict):
    call_id: str
    input: str
    chat_history: List[Dict[str, Any]]
    summary: str
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData


