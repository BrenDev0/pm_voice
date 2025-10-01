from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


from src.workflow.modules.appointments.google.services.client_manager import GoogleClientManager
from src.workflow.modules.appointments.google.services.calendar_serivce import GoogleCalendarService


class GoogleService:
    def __init__(
        self,
        calendar_service: GoogleCalendarService,
        client_manager: GoogleClientManager
        
    ):
        self.__calendar_service = calendar_service
        self.__client_manager = client_manager
       

  