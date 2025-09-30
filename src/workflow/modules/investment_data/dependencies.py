from fastapi import Depends

from src.workflow.modules.investment_data.agent import InvestmentDataAgent
from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from src.dependencies.services import get_llm_service, get_prompt_service

def get_iventstment_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> InvestmentDataAgent:
    

    return InvestmentDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service
    )