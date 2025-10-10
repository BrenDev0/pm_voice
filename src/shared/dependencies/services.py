from src.shared.services.speech.domain.speech_to_text import SpeechToText
from src.shared.services.speech.infrastructure.deepgram_speech_to_text_service import DeepgramSpeechToTextService
from src.shared.services.web_socket.services.transport import WebSocketTransportService

def get_ws_transport_service() -> WebSocketTransportService:
    return WebSocketTransportService()


def get_speech_to_text_service():
    return DeepgramSpeechToTextService()