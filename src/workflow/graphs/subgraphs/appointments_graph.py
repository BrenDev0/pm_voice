from langgraph.graph import StateGraph, START, END
from src.workflow.state import AppointmentData

def create_appointments_graph():
    graph = StateGraph(AppointmentData)

    return graph.compile()