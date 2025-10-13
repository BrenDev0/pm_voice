from typing import Union, List, Dict, Any
from uuid import UUID

from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.service import PromptService
from src.workflows.services.prompt.entities import Message
from src.workflows.modules.client_data.models import ClientState
from src.shared.services.web_socket.services.transport import WebSocketTransportService

from src.shared.utils.decorators.error_handler import error_handler



class ClientDataAgent:
    __MODULE = "client_data.agent"
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
    async def __get_prompt(
        self,
        state: ClientState,
        chat_history: List[Message]
    ):
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        system_message = f"""
        You are a personal data collector.
        Your job is to ask the client in a calm and friendly tone for any missing data that may be required.

        the data that you will be collecting:
        name - the clients full name
        email - the clients email address
        phone - the clients phone number

        this data is required for making appointments and for any information they client may be request, and to best help the client with thier needs.

        the missing data that you need to request:
        {missing_data}
        
        IMPORTANT
        - you will not ask for more than one data point at a time.
        - you will always response in a friendly manner.
        - you can explain why the data is required if necessary, but only if asked.

    """

        prompt = await self.__prompt_service.build_prompt(
            system_message=system_message,
            chat_history=chat_history,
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: Union[UUID, str],
        state: ClientState,
        chat_history: List[Message]
    ):
        
        prompt = await self.__get_prompt(
            chat_history=chat_history,
            state=state
        )
 
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=1.0
        ):
            print(chunk)
            await self.__ws_transport_service.send(
                connection_id=ws_connection_id,
                data={
                    "type": "transcription",
                    "text": chunk
                }
            )



        

        