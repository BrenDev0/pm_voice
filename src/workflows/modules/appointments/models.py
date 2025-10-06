from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentState(BaseModel):
    appointment_datetime: Optional[datetime] = None,
    date_available: bool = False

