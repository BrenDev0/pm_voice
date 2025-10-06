from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import os
from typing import List

from src.workflows.services.embedding.domain.embedding_service import EmbeddingService
from src.workflows.services.embedding.domain.models import SearchResult, EmbeddingConfig
from src.core.utils.decorators.error_handler import error_handler

class QdrantEmbeddingService(EmbeddingService):
    __MODULE = "embeddings.quadrant.service"
    def __init__(
            self,
            embedding_config: EmbeddingConfig = EmbeddingConfig()
        ):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        self.embedding_config = embedding_config
        
        self.embedding_model =  OpenAIEmbeddings(
            model=self.embedding_config.model_name,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    

    @error_handler(module=__MODULE)
    async def search_for_context(self, query, collection_name, top_k = 4):
        results: List[SearchResult] = await self.similarity_search(
            query=query,
            collection_name=collection_name,
            limit=top_k
        )
        
        if not results:
            return None
            
        return "\n\n".join([result.text for result in results])
        

    

    async def similarity_search(self, query, collection_name, limit = 4):
        query_embedding = await self.embedding_model.aembed_query(query)

        search_results = self.client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=limit,
            with_payload=True
        )

        return [
            SearchResult(
                text=item.payload["text"],
                metadata=item.payload.get("metadata", {}),
                item=item.score
            )
            for item in search_results
        ]