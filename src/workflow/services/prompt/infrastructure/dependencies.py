from fastapi import Depends

from src.workflow.services.prompt.prompt_service import PromptService
from src.workflow.services.embedding.embedding_service import EmbeddingService
from src.workflow.services.embedding.infrastructure.qdrant.dependencies import get_embedding_service



def get_prompt_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
) -> PromptService:
    return PromptService(
        embedding_service=embedding_service
    )