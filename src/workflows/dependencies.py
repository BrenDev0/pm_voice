from src.workflows.domain.services.llm_service import LlmService
from src.workflows.application.prompt_service import PromptService
from src.workflows.infrastructure.services.langchain_llm_service import LangchainLlmService

def get_llm_service() -> LlmService:
    return LangchainLlmService()

def get_prompt_service() -> PromptService:
    return PromptService()