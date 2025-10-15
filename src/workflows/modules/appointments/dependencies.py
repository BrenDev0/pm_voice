from fastapi import Depends

from src.workflows.modules.appointments.application.agent import AppointmentsAgent

from src.workflows.domain.services.llm_service import LlmService
from src.workflows.dependencies import get_prompt_service

from src.workflows.application.prompt_service import PromptService
from src.workflows.dependencies import get_llm_service

from src.shared.application.use_cases.stream_tts import StreamTTS
from src.shared.dependencies.services import get_stream_tts_use_case

from src.workflows.modules.appointments.domain.calendar_service import CalendarService
from src.workflows.modules.appointments.infrastructure.google.services.google_calendar_serivce import GoogleCalendarService

def get_calendar_service() -> CalendarService:
    return GoogleCalendarService()


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