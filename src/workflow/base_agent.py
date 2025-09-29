from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService
from src.workflow.state import State

class BaseAgent:
    def __init__(
        self, 
        llm_service: LlmService, 
        prompt_service: PromptService,
        system_message: str,
        state_field: str,
        max_tokens: int = None,
        temperature: float = 0.0,
        chat_history: bool = False,
        context: bool = False,
        context_collection_name: str = None,
        
    ):
        self._system_message = system_message
        self._state_field = state_field
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._llm_service = llm_service
        self._prompt_service = prompt_service
        self._chat_history = chat_history
        self._context = context
        self._context_collection_name = context_collection_name
      
    async def _get_prompt(
        self,
        state: State
    ):
        current_workflow_state = state[self._state_field]
        missing_data = [key for key, value in current_workflow_state.model_dump().items() if value is None]

        system_message = self._system_message.format(
            missing_data=missing_data
        )
       
        prompt = await self._prompt_service.custom_prompt_template(
            state=state,
            system_message=system_message,
            with_chat_history=self._chat_history
        )

        return prompt
    
    async def interact(
        self,
        state: State
    ):
        
        prompt = await self._get_prompt(state=state)

        llm = self._llm_service.get_llm(
            temperature=self._temperature,
            max_tokens=self._max_tokens
        )

        chain = prompt | llm

        response = chain.aivoke({"input": state["input"]})

        return response



        

        