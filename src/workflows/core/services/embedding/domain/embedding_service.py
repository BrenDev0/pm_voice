from abc import ABC, abstractmethod
from typing import List, Optional
from src.workflows.services.embedding.domain.models import SearchResult


class EmbeddingService(ABC):
    @abstractmethod
    def similarity_search(
        self,
        query: str,
        collection_name: str,
        limit: int = 4
    ) -> List[SearchResult]:
        raise NotImplementedError
    
    @abstractmethod
    async def search_for_context(
        self,
        query: str,
        collection_name: str,
        top_k: int = 4
    ) -> Optional[str]:
        raise NotImplementedError