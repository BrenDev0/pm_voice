import asyncio
import os
import uuid

from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService
from src.workflow.state import State



class Orchestrator:
    def __init__(self, llm_service: LlmService, prompt_service: PromptService):
        self.llm_service = llm_service
        self.prompt_service = prompt_service
      
    async def __get_prompt(
        self,
        state: State
    ):
        system_message =  """
        You are a helpful assistant you will help the client with what ever query they may have.
        """

        prompt = await self.prompt_service.custom_prompt_template(
            state=state,
            system_message=system_message
        )

        return prompt
    
    async def interact(
        self,
        state: State
    ):
        
        prompt = await self.__get_prompt(state=state)

        llm = self.llm_service.get_llm(
            temperature=1.0,
            max_tokens=100
        )

        chain = prompt | llm

        response = []
        accumulated_text = ""
        async for chunk in chain.astream({'input': state["input"]}):
            print(chunk.content)
            response.append(chunk.content)
            

        return " ".join(response)

        