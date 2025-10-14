import os
from typing import List

from src.shared.domain.entities import Message

class PromptService:
    
    async def build_prompt(
        self,  
        system_message: str, 
        input: str = None,
        chat_history: List[Message] = None,
        context: str = None
    ) -> str:
        messages = [
            system_message,
            f"You will always answer in {os.getenv('AGENT_LANGUAGE')}",
        ]
        
        if chat_history:
            messages = self.add_chat_history(chat_history=chat_history, messages=messages)

        if context:
            messages.append(f"\n\nYou have access to the following context: {context}")

        if input:
            messages.append(f"\n\nUser input: {input}")

        return " ".join(messages)

    @staticmethod
    def add_chat_history(chat_history: List[Message], messages: List[str]) -> List[str]:
        if chat_history:
            messages.append("\n\nCONVERSATION HISTORY:")
            for msg in chat_history:
                message_type = msg.type
                messages.append(f"{message_type}: {msg.content}")

        return messages
    
    
    
    