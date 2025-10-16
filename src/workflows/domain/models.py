from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvestmentState(BaseModel):
    type: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    action: Optional[str] = None


class AppointmentState(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    appointment_datetime: Optional[datetime] = None
    date_available: bool = False

class DataCollectorResponse(BaseModel):
    investment_data: InvestmentState
    appointment_data: AppointmentState
    client_intent: str 

