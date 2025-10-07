from src.workflows.services.llm.domain.llm_service import LlmService

from src.workflows.services.llm.infrastructure.langchain.langchain_llm_service import LangchainLlmService

def get_llm_service() -> LlmService:
    return LangchainLlmService()