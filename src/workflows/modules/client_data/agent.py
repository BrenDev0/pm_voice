from typing import Union, List, Dict, Any
from uuid import UUID

from src.workflows.core.services.llm.service import LlmService
from src.workflows.core.services.prompt.service import PromptService
from src.workflows.modules.client_data.models import ClientState
from src.core.services.web_socket.services.transport import WebSocketTransportService

from src.core.utils.decorators.error_handler import error_handler



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
        chat_history: List[Dict[str, Any]]
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

        prompt = await self.__prompt_service.custom_prompt_template(
            system_message=system_message,
            with_chat_history=True,
            chat_history=chat_history,
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: Union[UUID, str],
        state: ClientState,
        chat_history: List[Dict[str, Any]]
    ):
        
        prompt = await self.__get_prompt(
            chat_history=chat_history,
            state=state
        )

        llm = self.__llm_service.get_llm(
            temperature=1.0
        )

        chain = prompt | llm

        chunks = []
        async for chunk in chain.astream({}):
            await self.__ws_transport_service.send(
                connection_id=ws_connection_id,
                data=chunk
            )
        
        return "".join(chunks)



        

        