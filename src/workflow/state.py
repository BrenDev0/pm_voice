from typing_extensions import TypedDict
from typing import List, Dict, Any

from src.workflow.modules.appointments.models import AppointmentData
from src.workflow.modules.client_data.models import ClientData
from src.workflow.modules.investment_data.models import InvestmentData

class State(TypedDict):
    call_id: str
    input: str
    chat_history: List[Dict[str, Any]]
    summary: str
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData


