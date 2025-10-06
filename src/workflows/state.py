from typing_extensions import TypedDict
from typing import List, Dict, Any

from src.workflows.modules.appointments.models import AppointmentData
from src.workflows.modules.client_data.domain.models import ClientData
from src.workflows.modules.investment_data.domain.models import InvestmentData

class State(TypedDict):
    call_id: str
    input: str
    chat_history: List[Dict[str, Any]]
    summary: str
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData


