from workflow.services.embedding.infrastructure.qdrant.qdrant_embedding_service import QdrantEmbeddingService
from src.workflow.services.embedding.domain.embedding_service import EmbeddingService

def get_qdrant_embedding_service() -> EmbeddingService:
    return QdrantEmbeddingService()
