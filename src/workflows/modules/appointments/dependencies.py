from fastapi import Depends

from src.workflows.modules.appointments.application.agent import AppointmentsAgent

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.dependencies import get_prompt_service

from src.workflows.application.prompt_service import PromptService
from src.workflows.dependencies import get_llm_service

from src.api.websocket.transport import WebSocketTransportService
from src.shared.dependencies.services import get_ws_transport_service

def get_appoinments_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    ws_tranport_service: WebSocketTransportService = Depends(get_ws_transport_service)
    
) -> AppointmentsAgent:
    
    return AppointmentsAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        ws_transport_service=ws_tranport_service
    )