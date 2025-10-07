import asyncio
from typing import AsyncIterable
from deepgram import LiveTranscriptionEvents

from src.shared.services.speech.domain.speech_to_text import SpeechToText
from src.shared.services.speech.infrastructure.deepgram.utils.deepgram_ws_methods import (
    on_close, on_error, on_open, get_options, get_connection
)

class DeepgramSpeechToTextService(SpeechToText):
    async def transcribe(data_stream: AsyncIterable[bytes]) -> str:
        dg_connection = get_connection()
        options = get_options(
            model="nova",
            language="es"
        )

        if not dg_connection.start(options):
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
        async for chunk in data_stream:
            dg_connection.send(chunk)

        dg_connection.finish()
        await finished.wait()

        return " ".join(chunks)