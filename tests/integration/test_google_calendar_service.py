from dotenv import load_dotenv
load_dotenv()
import pytest
from datetime import datetime

from src.workflows.infrastructure.google.google_calendar_serivce import GoogleCalendarService
from src.workflows.dependencies import get_calendar_service


google_calendar_service: GoogleCalendarService = get_calendar_service()


@pytest.mark.asyncio
async def test_check_availability():
    start_time = datetime(year=2025, month=10, day=16, hour=15)
    appointment_datetime = start_time.isoformat()

    result = await google_calendar_service.check_availability(appointment_datetime=appointment_datetime)

    assert result