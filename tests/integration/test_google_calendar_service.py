from dotenv import load_dotenv
load_dotenv()
import pytest

from src.workflows.infrastructure.google.google_calendar_serivce import GoogleCalendarService
from src.workflows.dependencies import get_calendar_service


google_calendar_service: GoogleCalendarService = get_calendar_service()


@pytest.mark.asyncio
async def test_check_availability():
    appointment_datetime = "2025-10-18T15:00:00-06:00"

    result = await google_calendar_service.check_availability(appointment_datetime=appointment_datetime)

    assert result == False