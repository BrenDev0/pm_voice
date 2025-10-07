from fastapi import Depends

from src.workflows.modules.investment_data.agent.agent import InvestmentDataAgent

from src.workflows.core.services.llm.domain.llm_service import LlmService
from src.workflows.core.services.prompt.dependencies import get_prompt_service

from src.workflows.core.services.prompt.service import PromptService
from src.workflows.core.services.llm.infrastructure.dependencies import get_llm_service

from src.core.services.web_socket.services.transport import WebSocketTransportService
from src.core.services.web_socket.dependencies import get_ws_transport_service

def get_iventstment_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    ws_transport_service: WebSocketTransportService = Depends(get_ws_transport_service)
) -> InvestmentDataAgent:
    

    return InvestmentDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        ws_transport_service=ws_transport_service
    )