from vapi import Vapi
import os
from src.workflow.vapi.vapi_models import VapiVoice, VapiModel, VapiAssistant
from typing import List, Dict, Any

class VapiService:
    def __init__(self):
        self.__client: Vapi = Vapi(token=os.getenv("VAPI_PRIVATE_KEY"))
    
    @staticmethod
    def get_voice(
        provider: str,
        voice_id: str
    ) -> VapiVoice:
        return VapiVoice(
            provider=provider,
            voiceId=voice_id
        )
    
    @staticmethod
    def get_model(
        provider: str,
        model: str,
        temperature: float,
        messages: List[Dict[str, Any]]
    ) -> VapiModel:
        return VapiModel(
            provider=provider,
            model=model,
            temperature=temperature,
            messages=messages
        )
    
    def create_custom_assistant(
        self,
        first_message: str,
        name: str,
        model: VapiModel,
        voice: VapiVoice
    ) -> VapiAssistant:
        
        assistant: VapiAssistant = self.__client.assistants.create(
            name=name,
            first_message=first_message,
            model=model,
            voice=voice
        )

        return assistant
        


