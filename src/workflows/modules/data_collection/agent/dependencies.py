from fastapi import Depends

from src.workflows.modules.data_collection.agent.agent import DataCollector

from src.workflows.core.services.llm.domain.llm_service import LlmService
from src.workflows.core.services.llm.infrastructure.dependencies import get_llm_service

from src.workflows.core.services.prompt.service import PromptService
from src.workflows.core.services.prompt.dependencies import get_prompt_service

def get_data_collector(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> DataCollector:
    return DataCollector(
        llm_service=llm_service,
        prompt_service=prompt_service
    )