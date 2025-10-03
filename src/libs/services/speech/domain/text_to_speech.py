from abc import ABC, abstractmethod

class TextToSpeech(ABC):
    @abstractmethod
    def transcribe():
        raise NotImplementedError