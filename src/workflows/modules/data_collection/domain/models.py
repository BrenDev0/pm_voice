from pydantic import BaseModel

from src.workflows.modules.appointments.domain.models import AppointmentState
from src.workflows.modules.investment_data.domain.models import InvestmentState

class DataCollectorResponse(BaseModel):
    investment_data: InvestmentState
    appointment_data: AppointmentState
    client_intent: str 