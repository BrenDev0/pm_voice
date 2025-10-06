from workflows.services.llm.llm_service import LlmService

def get_llm_service() -> LlmService:
    return LlmService()