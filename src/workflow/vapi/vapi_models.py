from pydantic import  BaseModel
from typing import List, Dict, Any

class VapiModel(BaseModel):
    provider: str
    model: str
    temperature: float
    messages: List[Dict[str, Any]]


class VapiVoice(BaseModel):
    provider: str
    voiceId: str


class VapiAssistant(BaseModel):
    name: str
    first_message: str
