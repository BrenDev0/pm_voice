from typing import List, Union
from uuid import UUID
import datetime
from zoneinfo import ZoneInfo

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.application.prompt_service import PromptService
from src.shared.domain.entities import Message
from src.shared.application.use_cases.stream_tts import StreamTTS
from src.shared.utils.decorators.error_handler import error_handler
from src.workflows.domain.models import AppointmentState
from src.workflows.domain.services.calendar_service import CalendarService

class AppointmentsAgent:
    __MODULE = "appointments.agent"
    
    def __init__(
        self, 
        llm_service: LlmService,
        prompt_service: PromptService,
        calendar_service: CalendarService,  
        stream_tts: StreamTTS
    ):
        self.__llm_service = llm_service
        self.__prompt_service = prompt_service
        self.__calendar_service = calendar_service
        self.__stream_tts = stream_tts

    @error_handler(module=__MODULE)  
    def __get_prompt_data_collection(
        self, 
        state: AppointmentState,
        chat_history: List[Message],
        input: str
    ) -> str:
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        now = datetime.datetime.now(tz=ZoneInfo("America/Merida")).isoformat()
        system_message = f"""
        You are a personal data collector speaking with a client on a phone call to book thier appointment.
        Your job is to interact in a calm, friendly, and natural conversational tone, collecting any missing data needed for the appointment.

        The data that you will be collecting:
        name - the clients full name
        email - the clients email address  
        phone - the clients phone number
        appointment_datetime datestring

        the current date time is:
            {now}
            use this as a reference when adding appoinment_datetime

        This data is required for making appointments and for any information they client may be request, and to best help the client with thier needs.

        The missing data that you need to request:
        {missing_data}
        
        IMPORTANT:
        - you will not ask for a datetime untill all other fields are filled.
        - Personalize each response using information from the chat history and user input.
        - DO NOT repeat greetings, opening phrases, or explanations already used in the conversation.
        - Avoid robotic or scripted language; respond as a real person would on a phone call.
        - If the client asks why data is needed, explain briefly and naturally.
        - If you already have a piece of data, do not ask for it again.
        - Vary your language and sentence structure; do not start every response the same way.
        - Use context from previous exchanges to make the conversation flow smoothly.

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
    def __get_prompt_unavailible(
        self, 
        chat_history: List[Message],
        input: str
    ) -> str:
        system_message = f"""
        You are on a ohone call with a client whose making an appoinmnet but the date they have requested is unavailbale.
        Ask the client for another date time for the appoinment
        """
    
        prompt = self.__prompt_service.build_prompt(
            system_message=system_message,
            chat_history=chat_history,
            input=input
        )

        return prompt
    
    @error_handler(module=__MODULE)
    def __get_prompt_confirmation(
        self, 
        chat_history: List[Message],
        input: str
    ) -> str:
        system_message = f"""
        You are on a ohone call with a client whose making an appoinmnet please let the client know that thier appointmnet hase been made.
        Thank the client for thier time and ask if there is anything else you can be of help with.
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
        state: AppointmentState,
        chat_history: List[Message],
        input: str
    ):
        if state.appointment_datetime:
            available = await self.__calendar_service.check_availability(state.appointment_datetime.isoformat())
            if available:
                prompt = self.__get_prompt_confirmation(
                    chat_history=chat_history,
                    input=input
                )
            else: 
                prompt = self.__get_prompt_unavailible(
                    chat_history=chat_history,
                    input=input
                )
                state.appointment_datetime = None
        else: 
            prompt = self.__get_prompt_data_collection(
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