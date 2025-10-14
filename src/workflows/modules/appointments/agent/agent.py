# src/workflows/modules/client_data/application/client_data_agent.py
from typing import List
from uuid import UUID

from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.service import PromptService
from src.shared.domain.entities import Message
from src.api.websocket.transport import WebSocketTransportService
from src.shared.utils.decorators.error_handler import error_handler
from src.workflows.modules.appointments.domain.models import AppointmentState

class AppointmentsAgent:
    __MODULE = "appointments.agent"
    
    def __init__(
        self, 
        llm_service: LlmService,
        prompt_service: PromptService,  
        ws_transport_service: WebSocketTransportService
    ):
        self.__llm_service = llm_service
        self.__prompt_service = prompt_service
        self.__ws_transport_service = ws_transport_service

    @error_handler(module=__MODULE)  
    async def __get_system_prompt(self, state: AppointmentState) -> str:
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        
        return f"""
        You are a personal data collector speaking with a client on a phone call to book thier appoiintment.
        Your job is to interact in a calm, friendly, and natural conversational tone, collecting any missing data needed for the appointment.

        The data that you will be collecting:
        name - the clients full name
        email - the clients email address  
        phone - the clients phone number

        This data is required for making appointments and for any information they client may be request, and to best help the client with thier needs.

        The missing data that you need to request:
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

    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: UUID,
        state: AppointmentState,
        chat_history: List[Message]
    ):
        system_prompt = await self.__get_system_prompt(state)
        
        prompt = await self.__prompt_service.build_promt(
            system_message=system_prompt,
            chat_history=chat_history
        )

        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=1.0
        ):
            await self.__ws_transport_service.send(
                connection_id=ws_connection_id,
                data=chunk
            )