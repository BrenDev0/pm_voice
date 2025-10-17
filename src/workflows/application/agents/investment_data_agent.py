from typing import List, Union
from uuid import UUID

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.application.prompt_service import PromptService
from src.shared.domain.entities import Message
from src.workflows.domain.models import InvestmentState
from src.shared.application.use_cases.stream_tts import StreamTTS

from  src.shared.utils.decorators.error_handler import error_handler

class InvestmentDataAgent:
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
        state: InvestmentState,
        chat_history: List[Message],
        input: str
    ):
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        system_message = f"""
        You are a personal data collector speaking with a client on a phone call.
        Your job is to interact in a calm, friendly, and natural conversational tone, collecting any missing data needed for the clients investment needs.

        You offer propierties, apartments, and houses.
        You offer these produnts in the North, Central of Mérida or on the Yucatán coast
        You offer these products as rentals or purchases

        the data that you will be collecting:
        type(house, apartment, commercial, land, ect) - the  type of product the client is looking for or presenting
        location - where the client is looking for the product
        budget - the clients budget
        action(buy, rent, sell, ect.) - what the client wishes to do with the product

        this data is required for making appointments and for any information they client may be request, and to best help the client with thier needs.

        the missing data that you need to request:
        {missing_data}

        If there is no missing data summerize the data you have collected and let the client know that the data has been sent to an acesor, 
        then ask the client if they would prefer to make an apoinment to view all options or would prefer to have the data emailed to them
        
        IMPORTANT:
        - Personalize each response using information from the chat history and user input.
        - DO NOT repeat greetings, opening phrases, or explanations already used in the conversation.
        - Avoid robotic or scripted language; respond as a real person would on a phone call.
        - Only ask for one missing data point at a time.
        - If the client asks why data is needed, explain briefly and naturally.
        - If you already have a piece of data, do not ask for it again.
        - Vary your language and sentence structure; do not start every response the same way.
        - Use context from previous exchanges to make the conversation flow smoothly.
        - Do not respond with emojis

        Remember:
        - Be friendly and conversational.
        - Do not repeat yourself.
        - Use the chat history to avoid redundancy.

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
        state: InvestmentState,
        chat_history: List[Message],
        input: str
    ):
        
        
        prompt = self.__get_prompt(
            chat_history=chat_history,
            state=state,
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



        

        