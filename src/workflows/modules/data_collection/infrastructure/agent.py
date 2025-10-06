from src.workflows.services.llm.llm_service import LlmService
from src.workflows.services.prompt.prompt_service import PromptService
from src.workflows.state import State
from src.workflows.modules.data_collection.domain.models import DataCollectorResponse

from src.core.utils.decorators.error_handler import error_handler

class DataCollector:
    __MODULE = "data_collector.agent"
    def __init__(self, llm_service: LlmService, prompt_service: PromptService):
        self.llm_service = llm_service
        self.prompt_service = prompt_service
    
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
        - Review the latest client response and the chat history.
        - Return a JSON dictionary with the keys "investment_data", "client_data", and "appointment_data".
        - For each key, include only the fields for which you found new information. If you have no new data for a section, set its value to an empty object: {{}}
        - Use the exact field names as shown above.
        - Do not include any extra text or explanation, only the JSON object.

        Example output:
        {{
        "client_data": {{"name": "Juan Perez"}},
        "investment_data": {{"type": "house", "location": "Merida", "budget": 2000000, "action": "buy"}},
        "appointment_data": {{"appointment_datetime": "2024-07-01T10:00:00"}}
        }}

        Example output with no new data:
        {{
        "client_data": {{}},
        "investment_data": {{}},
        "appointment_data": {{}}
        }}
        """

        prompt = await self.prompt_service.custom_prompt_template(
            system_message=system_message,
            with_input=True,
            input_text=state['input'],
            with_chat_history=True,
            chat_history=state['chat_history']
        )

        return prompt
    
    @error_handler(module=__MODULE)
    async def interact(
        self,
        state: State
    ) -> DataCollectorResponse:
        
        prompt = await self.__get_prompt(state=state)

        llm = self.llm_service.get_llm(
            temperature=1.0
        )

        structured_llm = llm.with_structured_output(DataCollectorResponse)

        chain = prompt | structured_llm

        response = chain.aivoke({"input": state["input"]})

        return response



        

        