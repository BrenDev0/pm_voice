import asyncio
from typing import AsyncIterable, Any
import base64
from  deepgram import DeepgramClient, LiveTranscriptionEvents 
from src.shared.services.speech.domain.speech_to_text import SpeechToText
from src.shared.services.speech.infrastructure.deepgram_ws_methods import (
    on_close, on_error, on_open, get_options, get_connection
)

class DeepgramSpeechToTextService(SpeechToText):
    def __init__(
        self,
        model: str = "nova",
        language: str = "es"
    ):
        super().__init__()
        
        self.__options = get_options(
            model=model,
            language=language
        )

    async def transcribe(self, data_stream: AsyncIterable[bytes]) -> str:
        dg_connection = get_connection()
        
        if not dg_connection.start(self.__options):
            raise Exception("Error connecting to deepgram")
        
        print("Deepgram connection started")

        chunks = []
        finished = asyncio.Event()

        def on_transcript(result):
            sentence = result.channel.alternatives[0].transcript
            if sentence and len(sentence) > 0:
                print(f"Transcript: {sentence}")
                chunks.append(sentence)

        def on_close_event(*args, **kwargs):
            print("Deepgram connection closed")
            finished.set()

        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Close, on_close_event)

        # Send audio data as it arrives
        async for data in data_stream:
            chunk = self.__get_audio_bytes(data)
            dg_connection.send(chunk)

        dg_connection.finish()
        await finished.wait()

        return " ".join(chunks)

    def __get_audio_bytes(data: Any):
        audio_data = data.get("data")
        audio_bytes = base64.b64decode(audio_data)
        return audio_bytes