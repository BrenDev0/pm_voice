from pydantic import BaseModel

from src.workflow.state import InvestmentData, ClientData, AppointmentData

class DataCollectorResponse(BaseModel):
    investment_data: InvestmentData
    client_data: ClientData
    appointment_data: AppointmentData