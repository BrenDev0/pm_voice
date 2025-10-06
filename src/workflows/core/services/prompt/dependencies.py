from fastapi import Depends

from src.workflows.core.services.prompt.service import PromptService

from src.workflows.core.services.embedding.domain.embedding_service import EmbeddingService
from src.workflows.core.services.embedding.infrastructure.qdrant.dependencies import get_qdrant_embedding_service

def get_prompt_service(
    embedding_service: EmbeddingService = Depends(get_qdrant_embedding_service)
) -> PromptService:
    return PromptService(
        embedding_service=embedding_service
    )