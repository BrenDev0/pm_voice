from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService
from typing import List, Dict, Any
from src.workflow.modules.investment_data.models import InvestmentData


class InvestmentDataAgent:
    def __init__(self, llm_service: LlmService, prompt_service: PromptService):
        self.llm_service = llm_service
        self.prompt_service = prompt_service
      
    async def __get_prompt(
        self,
        state: InvestmentData,
        chat_history: List[Dict[str, Any]]
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

        prompt = await self.prompt_service.custom_prompt_template(
            system_message=system_message,
            with_chat_history=True,
            chat_history=chat_history,
        )

        return prompt
    
    async def interact(
        self,
        state: InvestmentData,
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



        

        