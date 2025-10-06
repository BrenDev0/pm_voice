from fastapi import Depends

from src.workflows.modules.investment_data.infrastructure.agent import InvestmentDataAgent

from src.workflows.services.llm.llm_service import LlmService
from src.workflows.services.prompt.infrastructure.dependencies import get_prompt_service

from workflows.services.prompt.prompt_service import PromptService
from src.workflows.services.llm.infrastructure.dependencies import get_llm_service

def get_iventstment_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> InvestmentDataAgent:
    

    return InvestmentDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service
    )