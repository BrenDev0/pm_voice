from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

class BaseAgent:
    def __init__(
        self, 
        llm_service: LlmService,
        prompt_service: PromptService,
        system_message: str,
        temperature: float = 0.0,
        
    ):
        self._system_message = system_message
        self._temperature = temperature
        self._llm_service = llm_service
        self._prompt_service = prompt_service
        

    async def _get_prompt(
        self,
    ):
        raise NotImplementedError("Subclasses must implement _get_prompt")
    
    async def interact(
        self
    ):
        
        prompt = await self._get_prompt()

        llm = self._llm_service.get_llm(
            temperature=self._temperature
        )

        chain = prompt | llm

        response = chain.aivoke({})

        return response



        

        