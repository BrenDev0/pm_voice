from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.service import PromptService
from src.workflows.models import State
from src.workflows.modules.data_collection.models import DataCollectorResponse

from src.shared.utils.decorators.error_handler import error_handler

class DataCollector:
    __MODULE = "data_collector.agent"
    def __init__(
        self, 
        llm_service: LlmService, 
        prompt_service: PromptService
    ):
        self.__llm_service = llm_service
        self.__prompt_service = prompt_service
    
    @error_handler(module=__MODULE)
    async def __get_prompt(
        self,
        state: State
    ):
        system_message = f"""
        You are a data extraction assistant for a real estate workflow. 
        Your job is to analyze the latest client response and the chat history to extract any information that matches the following fields:

        Investment Data: type (house, apartment, commercial, land), location, budget, action (buy, sell, rent)
        Client Data: name, email, phone
        Appointment Data: appointment_datetime

        CURRENT STATE:
        Investment Data: {state.get('investment_data')}
        Client Data: {state.get('client_data')}
        Appointment Data: {state.get('appointment_data')}

        Instructions:
        - Only extract and return fields that are explicitly mentioned in the latest client response or chat history.
        - If no new information is found for a section, set its value to an empty object: null.
        - Do NOT guess or invent any values.
        - Do NOT use example names, locations, or dates unless they are present in the input or chat history.
        """

        prompt = await self.__prompt_service.build_prompt(
            system_message=system_message,
            input=state['input'],
            chat_history=state['chat_history']
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        state: State
    ) -> DataCollectorResponse:
        
        prompt = await self.__get_prompt(state=state)

        response = await self.__llm_service.invoke_structured(
            prompt=prompt,
            response_model=DataCollectorResponse,
            temperature=0.0
        )

        return response



        

        