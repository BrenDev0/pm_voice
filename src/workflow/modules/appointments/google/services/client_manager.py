import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from src.utils.decorators.error_handler import error_handler

class GoogleClientManager:
    __MODULE = "google.service.clientManager"
    @error_handler(module=__MODULE)    
    def get_client(self) -> Credentials:
        """Create OAuth2 credentials object with client config"""
        
        return Credentials(
            token=None,
            refresh_token=None,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        )
    
    @error_handler(module=__MODULE)    
    async def get_credentialed_client(self) -> Credentials:        
        credentials = Credentials(
            token=None,
            refresh_token=os.getenv("REFRESH_TOKEN"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        )
        
        # Refresh the access token
        await self.refresh_access_token(credentials)
        
        return credentials
            
      
    @error_handler(module=__MODULE)    
    async def refresh_access_token(self, credentials: Credentials) -> str:
        request = Request()
        
        # Refresh the credentials
        credentials.refresh(request)
        
        return credentials.token

       