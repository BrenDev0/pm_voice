from fastapi import Depends

from src.workflow.base_agent import BaseAgent
from src.workflow.services.llm_service import LlmService
from src.workflow.services.prompt_service import PromptService

from src.dependencies.services import get_llm_service, get_prompt_service

def get_client_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> BaseAgent:
    system_message_template = """
        You are a personal data collector.
        Your job is to ask the client in a calm and friendly tone for any missing data that may be required.

        the data that you will be collecting:
        name - the clients full name
        email - the clients email address
        phone - the clients phone number

        this data is required for making appointments and for any information they client may be request

        the missing data that you need to request:
        {missing_data}
        
        IMPORTANT
        - you will not ask for more than one data point at a time.
        - you will always response in a friendly manner.
        - you can explain why the data is required if necessary, but only  if asked.

    """

    return BaseAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        system_message_template=system_message_template,
        state_field="client_data",
        max_tokens=500,
        temperature=0.2,
        chat_history=True
    )