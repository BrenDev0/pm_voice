from src.workflows.core.services.embedding.infrastructure.qdrant.qdrant_embedding_service import QdrantEmbeddingService
from src.workflows.core.services.embedding.domain.embedding_service import EmbeddingService

def get_qdrant_embedding_service() -> EmbeddingService:
    return QdrantEmbeddingService()
