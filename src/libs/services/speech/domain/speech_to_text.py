from abc import ABC, abstractmethod

class SpeechToText(ABC):
    @abstractmethod
    def transcribe():
        raise NotImplementedError