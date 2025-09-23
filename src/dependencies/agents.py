from fastapi import Depends

from src.dependencies.services import get_llm_service, get_prompt_service

from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from src.workflow.agents.orchestrator.orchestrator_agent import Orchestrator


def get_orchestrator_agent(
    llm_Service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> Orchestrator: 
    return Orchestrator(
        llm_service=llm_Service,
        prompt_service=prompt_service
    )
