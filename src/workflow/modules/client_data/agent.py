from workflow.services.llm.llm_service import LlmService
from workflow.services.prompt.prompt_service import PromptService
from src.workflow.modules.client_data.models import ClientData
from typing import List, Dict, Any

from src.libs.infrastructure.utils.decorators.error_handler import error_handler



class ClientDataAgent:
    __MODULE = "client_data.agent"
    def __init__(self, llm_service: LlmService, prompt_service: PromptService):
        self.llm_service = llm_service
        self.prompt_service = prompt_service

    @error_handler(module=__MODULE)  
    async def __get_prompt(
        self,
        state: ClientData,
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

        prompt = await self.prompt_service.custom_prompt_template(
            system_message=system_message,
            with_chat_history=True,
            chat_history=chat_history,
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        state: ClientData,
        chat_history: List[Dict[str, Any]]
    ):
        
        prompt = await self.__get_prompt(
            chat_history=chat_history,
            state=state
        )

        llm = self.llm_service.get_llm(
            temperature=1.0
        )

        chain = prompt | llm

        response = chain.aivoke({})

        return response



        

        