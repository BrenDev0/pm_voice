from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentState(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    appointment_datetime: Optional[datetime] = None
    date_available: bool = False

