from fastapi import Depends

from workflows.modules.client_data.agent import ClientDataAgent

from src.workflows.core.services.llm.service import LlmService
from src.workflows.core.services.prompt.dependencies import get_prompt_service

from workflows.core.services.prompt.service import PromptService
from src.workflows.core.services.llm.dependencies import get_llm_service

def get_client_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> ClientDataAgent:
    
    return ClientDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service
    )
    
