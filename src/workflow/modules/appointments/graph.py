from langgraph.graph import  StateGraph, START, END
from  fastapi import Depends

from src.workflow.modules.appointments.agent import ApointmentsAgent
from src.workflow.modules.appointments.models import AppointmentData
from src.workflow.modules.appointments.dependencies import get_appoinments_agent

def create_appointments_graph(
    appoinment_agent: ApointmentsAgent = Depends(get_appoinments_agent)
):
    graph = StateGraph(AppointmentData)

    def router(state: AppointmentData):
        pass

    async def get_datetime_node(state: AppointmentData):
        response = await appoinment_agent.interact({"input": state["input"]})

        return {"appointment_datetime": response}

    async def check_availability_node(state: AppointmentData):
        pass

    async def unavailable_node(state: AppointmentData):
        pass

    async def confirmation_node(state: AppointmentData):
        pass

    graph.add_node("get_datetime", get_datetime_node)
    graph.add_node("check_availability", check_availability_node)
    graph.add_node("unavailable", unavailable_node)
    graph.add_node("confirmation", confirmation_node)



    return graph.compile()
