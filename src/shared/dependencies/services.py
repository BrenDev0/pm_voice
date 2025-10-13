from fastapi import Depends
from src.shared.services.speech.domain.speech_to_text import SpeechToText
from src.shared.services.speech.domain.text_to_speech import TextToSpeech
from src.shared.services.speech.infrastructure.deepgram_speech_to_text_service import DeepgramSpeechToTextService
from src.shared.services.web_socket.services.transport import WebSocketTransportService
from src.shared.application.use_cases.stream_tts import StreamTTS
from src.shared.services.speech.infrastructure.deepgram_text_to_speech_service import DeepgramTextToSpeechService

def get_ws_transport_service() -> WebSocketTransportService:
    return WebSocketTransportService()


def get_speech_to_text_service() -> SpeechToText:
    return DeepgramSpeechToTextService(
        model="nova",
        language="es"
    )

def get_text_to_speech_service() -> TextToSpeech:
    return DeepgramTextToSpeechService()

def get_stream_tts_use_case(
    ws_tranport_service: WebSocketTransportService = Depends(get_ws_transport_service),
    tts_service: TextToSpeech = Depends(get_text_to_speech_service)
):
    return StreamTTS(
        ws_tansport_service=ws_tranport_service,
        tts_service=tts_service
    )