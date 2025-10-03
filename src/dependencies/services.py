from fastapi import Depends

from src.workflow.services.prompt_service import PromptService
from src.workflow.services.embedding_service import EmbeddingService
from src.workflow.services.llm_service import LlmService

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

def get_llm_service() -> LlmService:
    return LlmService()

def get_prompt_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> PromptService:
    return PromptService(
        embedding_service=embedding_service
    )