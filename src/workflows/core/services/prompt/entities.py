from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    AI = "ai"
    HUMAN = "human"

class Message(BaseModel):
    type: MessageType
    content: str