from typing import Union
from uuid import UUID

from src.workflows.core.services.llm.service import LlmService
from src.workflows.core.services.prompt.service import PromptService
from src.core.services.web_socket.services.transport import WebSocketTransportService

from src.core.utils.decorators.error_handler import error_handler

class ApointmentsAgent:
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
    async def __get_prompt(
        self
    ):
        system_message = """
        You are an appoinment maker.
        Your job is to ask the client in a calm and friendly tone for the desired date and time for thier appoinment.
        """

        prompt = await self.__prompt_service.custom_prompt_template(
            system_message=system_message
        )

        return prompt
    
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        ws_connection_id: Union[UUID, str]
    ):
        
        prompt = await self.__get_prompt()

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



        

        