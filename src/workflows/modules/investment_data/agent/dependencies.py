from fastapi import Depends

from src.workflows.modules.investment_data.agent.agent import InvestmentDataAgent

from src.workflows.services.llm.domain.llm_service import LlmService
from src.workflows.services.prompt.dependencies import get_prompt_service

from src.workflows.services.prompt.service import PromptService
from src.workflows.services.llm.infrastructure.dependencies import get_llm_service

from src.shared.application.use_cases.stream_tts import StreamTTS
from src.shared.dependencies.services import get_stream_tts_use_case

def get_iventstment_data_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    stream_tts: StreamTTS = Depends(get_stream_tts_use_case)
) -> InvestmentDataAgent:
    

    return InvestmentDataAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        stream_tts=stream_tts
    )