from src.workflows.domain.services.llm_service import LlmService
from src.workflows.application.prompt_service import PromptService
from src.shared.domain.models import State
from src.workflows.domain.models import DataCollectorResponse
import datetime 
from zoneinfo import ZoneInfo

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
    def __get_prompt(
        self,
        state: State
    ):
        now = datetime.datetime.now(tz=ZoneInfo("America/Merida")).isoformat()
        system_message = f"""
        You are an assistant for a real estate workflow. 
        Your job is to analyze the latest client response and the chat history to:

        1. Extract any information that matches the following fields:
        - Investment Data: type (house, apartment, commercial, land), location, budget, action (buy, sell, rent)
        - Appointment Data: appointment_datetime, name, email, phone
        the current date time is:
            {now}
            use this as a reference when adding appoinment_datetime

        2. Determine the client's intent:
        - If the client is showing intent to make an appointment, set client_intent to "appointment".
        - If the client is showing interest in investments, opportunities, or services offered, set client_intent to "investment".
        - If the intent is unclear, set client_intent to "unknown".

        CURRENT STATE:
        Investment Data: {state.get('investment_data')}
        Appointment Data: {state.get('appointment_data')}

        Instructions:
        - Only extract and return fields that are explicitly mentioned in the latest client response or chat history.
        - If no new information is found for a section, set its value to null.
        - Do NOT guess or invent any values.
        - Do NOT use example names, locations, or dates unless they are present in the input or chat history.
        - Use natural, concise language.
        - Do NOT use emojis or special characters.
        - For client_intent, always choose the most relevant option based on the client's words.
        - If the client provides both appointment and investment information, set client_intent to the one most recently discussed.
        """

        prompt = self.__prompt_service.build_prompt(
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
        
        prompt = self.__get_prompt(state=state)

        response = await self.__llm_service.invoke_structured(
            prompt=prompt,
            response_model=DataCollectorResponse,
            temperature=0.0
        )

        return response



        

        