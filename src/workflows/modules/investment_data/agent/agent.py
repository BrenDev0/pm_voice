from typing import List, Union
from uuid import UUID

from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.service import PromptService
from src.shared.domain.entities import Message
from src.workflows.modules.investment_data.models import InvestmentState
from src.api.websocket.transport import WebSocketTransportService

from  src.shared.utils.decorators.error_handler import error_handler

class InvestmentDataAgent:
    __MODULE = "investment_data.agent"
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
        state: InvestmentState,
        chat_history: List[Message]
    ):
        missing_data = [key for key, value in state.model_dump().items() if value is None]
        system_message = f"""
        You are an investment data collector.
        Your job is to ask the client in a calm and friendly tone for any missing data that may be required.

        the data that you will be collecting:
        type(house, apartment, commercial, land, ect) - the  type of product the client is looking for or presenting
        location - where the client is looking for the product
        budget - the clients budget
        action(buy, rent, sell, ect.) - what the client wisheto do with the product

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
        state: InvestmentState,
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
            await self.__ws_transport_service.send(
                connection_id=ws_connection_id,
                data=chunk
            )



        

        