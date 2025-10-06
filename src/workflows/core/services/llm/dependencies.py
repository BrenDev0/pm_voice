from src.workflows.core.services.llm.service import LlmService

def get_llm_service() -> LlmService:
    return LlmService()