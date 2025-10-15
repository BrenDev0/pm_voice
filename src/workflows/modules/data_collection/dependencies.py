from fastapi import Depends

from src.workflows.modules.data_collection.application.agent import DataCollector

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.dependencies import get_llm_service

from src.workflows.application.prompt_service import PromptService
from src.workflows.dependencies import get_prompt_service

def get_data_collector(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> DataCollector:
    return DataCollector(
        llm_service=llm_service,
        prompt_service=prompt_service
    )