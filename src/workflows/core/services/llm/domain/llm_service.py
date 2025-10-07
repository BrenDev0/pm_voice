# src/workflows/core/services/llm/domain/llm_service.py
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List

class LlmService(ABC):
    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> AsyncGenerator[str, None]:
        raise NotImplementedError
    
    @abstractmethod
    async def invoke(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = None
    ) -> str:
        raise NotImplementedError