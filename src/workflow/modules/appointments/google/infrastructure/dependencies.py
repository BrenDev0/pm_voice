from fastapi import Depends

from src.workflow.modules.appointments.google.infrastructure.services.service import GoogleService
from src.workflow.modules.appointments.google.infrastructure.services.calendar_serivce import GoogleCalendarService
from src.workflow.modules.appointments.google.infrastructure.services.client_manager import GoogleClientManager


def get_calendar_service() -> GoogleCalendarService:
    return GoogleCalendarService()

def get_client_manager() -> GoogleClientManager:
    return GoogleClientManager()


def get_google_service(
    calendar_service: GoogleCalendarService = Depends(get_calendar_service),
    client_manager: GoogleClientManager = Depends(get_client_manager)
    
):
    return GoogleService(
        calendar_service=calendar_service,
        client_manager=client_manager
    )