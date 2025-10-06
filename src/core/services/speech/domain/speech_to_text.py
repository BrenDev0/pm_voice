from abc import ABC, abstractmethod
from typing import AsyncIterable

class SpeechToText(ABC):
    @abstractmethod
    def transcribe(data_stream: AsyncIterable[bytes]) -> str:
        raise NotImplementedError