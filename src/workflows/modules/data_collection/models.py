from pydantic import BaseModel

from src.workflows.core.state import InvestmentData, ClientData, AppointmentData

class DataCollectorResponse(BaseModel):
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData