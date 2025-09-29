from pydantic import BaseModel
from typing import Optional



class ClientData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
