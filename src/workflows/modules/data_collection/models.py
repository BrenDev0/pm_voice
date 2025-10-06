from pydantic import BaseModel

from src.workflows.modules.appointments.models import AppointmentState
from src.workflows.modules.client_data.models import ClientState
from src.workflows.modules.investment_data.models import InvestmentState

class DataCollectorResponse(BaseModel):
    investment_data: InvestmentState
    client_data: ClientState
    appointment_data: AppointmentState