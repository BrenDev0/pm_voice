from typing import Union
from uuid import UUID

from src.shared.domain.text_to_speech import TextToSpeech
from src.api.websocket.transport import WebSocketTransportService

class StreamTTS():
    def __init__(
        self,
        tts_service: TextToSpeech,
        ws_tansport_service: WebSocketTransportService
    ):
        self.__tts_service = tts_service
        self.__ws_tranport_service = ws_tansport_service

    
    async def execute(
        self, 
        ws_connection_id: Union[UUID, str], 
        text: str
    ):
        audio_chunk = self.__tts_service.transcribe(text)
    
        await self.__ws_tranport_service.send(ws_connection_id,{
            "type": "audio_response",
            "audio_data": audio_chunk
        })
    
        