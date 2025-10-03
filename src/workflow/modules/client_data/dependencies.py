from fastapi import Depends

from src.workflow.modules.client_data.agent import ClientDataAgent

from workflow.services.llm.llm_service import LlmService
from src.workflow.services.prompt.infrastructure.dependencies import get_prompt_service

from workflow.services.prompt.prompt_service import PromptService
from src.workflow.services.llm.infrastructure.dependencies import get_llm_service

def get_client_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> ClientDataAgent:
    
    return ClientDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service
    )
    
