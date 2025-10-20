from typing_extensions import TypedDict
from typing import List, Dict, Any

from src.workflows.domain.models import AppointmentState
from src.workflows.domain.models import InvestmentState

class State(TypedDict):
    call_id: str
    input: str
    chat_history: List[Dict[str, Any]]
    summary: str
    response: str
    investment_data: InvestmentState
    appointment_data: AppointmentState
    client_intent: str
    end_call: bool
