from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


from src.workflows.modules.appointments.google.infrastructure.services.client_manager import GoogleClientManager
from src.workflows.modules.appointments.google.infrastructure.services.calendar_serivce import GoogleCalendarService


class GoogleService:
    def __init__(
        self,
        calendar_service: GoogleCalendarService,
        client_manager: GoogleClientManager
        
    ):
        self.calendar_service = calendar_service
        self.client_manager = client_manager
       

   