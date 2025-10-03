from fastapi import Depends

from src.workflow.modules.data_collection.infrastructure.agent import DataCollector

from src.workflow.services.llm.llm_service import LlmService
from src.workflow.services.llm.infrastructure.dependencies import get_llm_service

from workflow.services.prompt.prompt_service import PromptService
from src.workflow.services.prompt.infrastructure.dependencies import get_prompt_service

def get_data_collector(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> DataCollector:
    return DataCollector(
        llm_service=llm_service,
        prompt_service=prompt_service
    )