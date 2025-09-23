from fastapi import Depends

from src.dependencies.services import get_llm_service, get_prompt_service

from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from workflow.agents.data_collection.data_collector import DataCollector


def get_data_collector(
    llm_Service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> DataCollector: 
    return DataCollector(
        llm_service=llm_Service,
        prompt_service=prompt_service
    )


