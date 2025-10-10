import asyncio
from typing import Any, Dict
import base64
import os
from deepgram import DeepgramClient
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import ListenV1SocketClientResponse
#### https://github.com/deepgram/deepgram-python-sdk/blob/main/docs/Migrating-v3-to-v5.md#installation-changes

from src.shared.services.speech.domain.speech_to_text import SpeechToText

class DeepgramSpeechToTextService(SpeechToText):
    def __init__(self, model: str = "nova-2", language: str = "es"):
        super().__init__()
        self.__model = model
        self.__language = language
        self.active_sessions: Dict[str, Any] = {}

    async def start_transcription_session(self, websocket):
        client = DeepgramClient()
        session_id = f"session_{id(websocket)}"
        
        try:

            session_data = {
                "connection": connection,
                "transcript_parts": [],
                "websocket": websocket,
                "client": client
            }

            with client.listen.v2.connect(
                model="flux-general-en",
                encoding="linear16",
                sample_rate="16000"
            ) as connection:
                def on_message(message):
                    print(f"Received {message.type} event")

                connection.on(EventType.OPEN, lambda _: print("Connection opened"))
                connection.on(EventType.MESSAGE, on_message)
                connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
                connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

                connection.start_listening()

            # def on_message(self, result, **kwargs):
            #     sentence = result.channel.alternatives[0].transcript
            #     if sentence and len(sentence) > 0:
            #         print(f"🎤 {sentence}")
            #         session_data["transcript_parts"].append(sentence)
            #         asyncio.create_task(websocket.send_json({
            #             "type": "partial_transcription",
            #             "text": sentence,
            #             "is_final": True
            #         }))

            # self.active_sessions[session_id] = session_data
            # return session_id

        except Exception as e:
            print(f"ERROR starting session: {e}")
            return None

    async def send_audio_chunk(self, session_id: str, audio_data: str):
        print("sending")
        if session_id not in self.active_sessions:
            return
        
        session = self.active_sessions[session_id]
        print("session found")
        connection = session["connection"]
        
        try:
            audio_bytes = self.get_audio_bytes(audio_data)
            if audio_bytes:
                connection.send(audio_bytes)
        except Exception as e:
            print(f"Error sending chunk: {e}")

    async def end_transcription_session(self, session_id: str) -> str:
        if session_id not in self.active_sessions:
            return ""
        
        session = self.active_sessions[session_id]
        connection = session["connection"]
        transcript_parts = session["transcript_parts"]
        
        try:
            connection.finish()  
            await asyncio.sleep(1)
            
            full_transcript = " ".join(transcript_parts)
            
            del self.active_sessions[session_id]
            
            return full_transcript
            
        except Exception as e:
            print(f"Error ending session: {e}")
            return " ".join(transcript_parts)

    async def cleanup_session(self, session_id: str):

        if session_id in self.active_sessions:
            try:
                session = self.active_sessions[session_id]
                session["connection"].finish()
                del self.active_sessions[session_id]
            except Exception as e:
                print(f"Error cleaning up session: {e}")

    def get_audio_bytes(self, data: Any) -> bytes:
        try:
            if isinstance(data, str):
                return base64.b64decode(data)
            elif isinstance(data, bytes):
                return data
            else:
                return b""
        except Exception as e:
            print(f"Error decoding audio: {e}")
            return b""