from fastapi import Depends

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.domain.services.calendar_service import CalendarService

from src.workflows.application.prompt_service import PromptService
from src.workflows.application.agents.investment_data_agent import InvestmentDataAgent
from src.workflows.application.agents.data_collection_agent import DataCollector
from src.shared.application.use_cases.stream_tts import StreamTTS
from src.workflows.application.agents.appointments_data_agent import AppointmentsAgent

from src.workflows.infrastructure.google.services.google_calendar_serivce import GoogleCalendarService
from src.workflows.infrastructure.services.langchain_llm_service import LangchainLlmService

from src.shared.dependencies.services import get_stream_tts_use_case

def get_calendar_service() -> CalendarService:
    return GoogleCalendarService()


def get_llm_service() -> LlmService:
    return LangchainLlmService()

def get_prompt_service() -> PromptService:
    return PromptService()


def get_appoinments_agent(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    stream_tts: StreamTTS = Depends(get_stream_tts_use_case),
    calendar_service: CalendarService = Depends(get_calendar_service)
    
) -> AppointmentsAgent:
    
    return AppointmentsAgent(
        llm_service=llm_service,
        prompt_service=prompt_service,
        stream_tts=stream_tts,
        calendar_service=calendar_service
    )

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

def get_data_collector(
    llm_service: LlmService = Depends(get_llm_service),
    prompt_service: PromptService = Depends(get_prompt_service)
) -> DataCollector:
    return DataCollector(
        llm_service=llm_service,
        prompt_service=prompt_service
    )
