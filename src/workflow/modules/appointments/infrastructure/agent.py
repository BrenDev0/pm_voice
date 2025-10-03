from workflow.services.llm.llm_service import LlmService
from workflow.services.prompt.prompt_service import PromptService

from src.libs.infrastructure.utils.decorators.error_handler import error_handler

class ApointmentsAgent:
    __MODULE = "appointments.agent"
    def __init__(self, llm_service: LlmService, prompt_service: PromptService):
        self.llm_service = llm_service
        self.prompt_service = prompt_service
    
    @error_handler(module=__MODULE)
    async def __get_prompt(
        self
    ):
        system_message = """
        You are an appoinment maker.
        Your job is to ask the client in a calm and friendly tone for the desired date and time for thier appoinment.
        """

        prompt = await self.prompt_service.custom_prompt_template(
            system_message=system_message
        )

        return prompt
    
    
    @error_handler(module=__MODULE)
    async def interact(
        self
    ):
        
        prompt = await self.__get_prompt()

        llm = self.llm_service.get_llm(
            temperature=1.0
        )

        chain = prompt | llm

        response = chain.aivoke({})

        return response.content.strip()



        

        