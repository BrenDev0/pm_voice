from deepgram import DeepgramClient
import base64
from src.shared.domain.text_to_speech import TextToSpeech

class DeepgramTextToSpeechService(TextToSpeech):
    def  transcribe(self, text: str):
        deepgram = DeepgramClient()
        if text:
            response = deepgram.speak.v1.audio.generate(
                text=text,
                model="aura-2-celeste-es"
            )
        
            audio_bytes = b"".join(response)      
            
            return base64.b64encode(audio_bytes).decode('utf-8')