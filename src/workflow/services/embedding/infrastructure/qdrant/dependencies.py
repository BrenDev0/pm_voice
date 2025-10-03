from workflow.services.embedding.embedding_service import EmbeddingService

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
