from fastapi import Depends

from src.workflow.base_agent import BaseAgent
from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from src.dependencies.services import get_llm_service, get_prompt_service

def get_appoinments_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> BaseAgent:
    system_message_template = """
        You are an appoinment maker.
        Your job is to ask the client in a calm and friendly tone for the desired date and time for thier appoinment.
    """

    return BaseAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        system_message_template=system_message_template,
        state_field="appointment_data",
        max_tokens=500,
        temperature=0.2,
        chat_history=True
    )