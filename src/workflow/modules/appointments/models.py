from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentData(BaseModel):
    appointment_datetime: Optional[datetime] = None 