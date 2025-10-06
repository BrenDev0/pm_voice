import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from src.workflows.modules.appointments.services.calendar.infrastructure.google.decorators.errors import google_api_error_handler

class GoogleClientManager:
    __MODULE = "google.service.clientManager"
        
    
    @google_api_error_handler(module=__MODULE)    
    async def get_credentialed_client(self) -> Credentials:        
        credentials = Credentials(
            token=None,
            refresh_token=os.getenv("PM_GOOGLE_REFRESH_TOKEN"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        )
        
        # Refresh the access token
        await self.refresh_access_token(credentials)
        
        return credentials
    
    def build_service(self, service_name: str, version: str = 'v3' ):
        credentials = self.get_credentialed_client()
        return build(
            serviceName=service_name,
            version=version,
            credentials=credentials
        )
      
    @google_api_error_handler(module=__MODULE)    
    async def refresh_access_token(self, credentials: Credentials) -> str:
        request = Request()
        
        # Refresh the credentials
        credentials.refresh(request)
        
        return credentials.token

       