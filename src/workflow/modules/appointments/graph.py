from langgraph.graph import  StateGraph, START, END
from  fastapi import Depends

from src.workflow.base_agent import BaseAgent

from src.workflow.state import State
from src.workflow.modules.appointments.dependencies import get_appoinments_agent

def create_appointments_graph(
    appoinment_agent: BaseAgent = Depends(get_appoinments_agent)
):
    graph = StateGraph(State)

    def router(state: State):
        pass

    async def get_datetime_node(state: State):
        response = await appoinment_agent.interact({"input": state["input"]})

        state["appointment_data"].appointment_datetime = response
        return state["appointment_data"]

    async def check_availability_node(state: State):
        pass

    async def unavailable_node(state: State):
        pass

    async def confirmation_node(state: State):
        pass

    graph.add_node("get_datetime", get_datetime_node)
    graph.add_node("check_availability", check_availability_node)
    graph.add_node("unavailable", unavailable_node)
    graph.add_node("confirmation", confirmation_node)



    return graph.compile()
