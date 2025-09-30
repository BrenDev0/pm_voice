from fastapi import Depends

from src.workflow.modules.client_data.agent import ClientDataAgent
from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from src.dependencies.services import get_llm_service, get_prompt_service

def get_client_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> ClientDataAgent:
    
    return ClientDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service
    )
    
