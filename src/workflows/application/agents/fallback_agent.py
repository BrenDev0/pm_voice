from typing import List, Union
from uuid import UUID

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.application.prompt_service import PromptService
from src.shared.domain.entities import Message
from src.shared.application.use_cases.stream_tts import StreamTTS

from  src.shared.utils.decorators.error_handler import error_handler

class FallbackAgent:
    __MODULE = "investment_data.agent"
    def __init__(
        self, 
        llm_service: LlmService, 
        prompt_service: PromptService,
        stream_tts: StreamTTS
    ):
        self.__llm_service = llm_service
        self.__prompt_service = prompt_service
        self.__stream_tts = stream_tts
    
    @error_handler(module=__MODULE)
    def __get_prompt(
        self,
        chat_history: List[Message],
        input: str
    ):
        system_message = f"""
        You are a concise customer-facing phone assistant for a real estate company serving Mérida and the Yucatán coast.
        If the client asks for something outside the company's scope, or the intent is unclear, respond with a single short sentence that:
        - States the company only provides real estate services in Mérida/Yucatán (buy/sell/rent, property info, appointments).
        - Offers to schedule an appointment or help with finding an investment that suits thier needs.
        - Does NOT invent any facts, does NOT explain reasoning, and keeps the reply suitable for immediate TTS playback.

        Examples (client -> agent):
        - "Can you file my taxes?" -> "We only handle real estate services in Mérida/Yucatán coast; I can schedule an appointment or help you find your right investment."
        - "I want info" -> "Do you want help buying, selling, renting, or to schedule an appointment?"

        Keep replies short (one sentence), polite, and phone-call natural.
        """

        prompt = self.__prompt_service.build_prompt(
            system_message=system_message,
            chat_history=chat_history,
            input=input
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: Union[UUID, str],
        chat_history: List[Message],
        input: str
    ):
        
        
        prompt = self.__get_prompt(
            chat_history=chat_history,
            input=input
        )
        chunks = []
        sentence = ""
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=0.3
        ):
            chunks.append(chunk)
            sentence += chunk
            # Check for sentence-ending punctuation
            if any(p in chunk for p in [".", "?", "!"]) and len(sentence) > 10:
                await self.__stream_tts.execute(
                    ws_connection_id=ws_connection_id,
                    text=sentence.strip()
                )
                sentence = ""

        # Send any remaining text after the stream ends
        if sentence.strip():
            await self.__stream_tts.execute(
                ws_connection_id=ws_connection_id,
                text=sentence.strip()
            )
            
        return "".join(chunks)



        

        