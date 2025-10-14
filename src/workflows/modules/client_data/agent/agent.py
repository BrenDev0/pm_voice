from typing import Union, List, Dict, Any
from uuid import UUID

from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.service import PromptService
from src.shared.domain.entities import Message
from src.workflows.modules.client_data.models import ClientState
from src.shared.application.use_cases.stream_tts import StreamTTS

from src.shared.utils.decorators.error_handler import error_handler

class ClientDataAgent:
    __MODULE = "client_data.agent"
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
    async def __get_prompt(
        self,
        state: ClientState,
        chat_history: List[Message],
        input: str
    ):
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        system_message = f"""
        You are a personal data collector speaking with a client on a phone call.
        Your job is to interact in a calm, friendly, and natural conversational tone, collecting any missing data needed for appointments or information requests.

        Data to collect:
        - Full name
        - Email address
        - Phone number

        Missing data to request:
        {missing_data}

        IMPORTANT:
        - Personalize each response using information from the chat history and user input.
        - DO NOT repeat greetings, opening phrases, or explanations already used in the conversation.
        - Avoid robotic or scripted language; respond as a real person would on a phone call.
        - Only ask for one missing data point at a time.
        - If the client asks why data is needed, explain briefly and naturally.
        - If you already have a piece of data, do not ask for it again.
        - Vary your language and sentence structure; do not start every response the same way.
        - Use context from previous exchanges to make the conversation flow smoothly.

        Remember:
        - Be friendly and conversational.
        - Do not repeat yourself.
        - Use the chat history to avoid redundancy.

    """

        prompt = await self.__prompt_service.build_prompt(
            system_message=system_message,
            chat_history=chat_history,
            input=input
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: Union[UUID, str],
        state: ClientState,
        chat_history: List[Message],
        input: str
    ):
        
        prompt = await self.__get_prompt(
            chat_history=chat_history,
            state=state,
            input=input
        )
        chunks = []
        sentence = ""
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=0.5
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

    
        



        

        