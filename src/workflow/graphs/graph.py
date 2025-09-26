import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.workflow.graphs.subgraphs.appointments_graph import create_appointments_graph
from src.workflow.graphs.subgraphs.client_data_graph import create_client_data_graph
from src.workflow.graphs.subgraphs.invenstment_data_graph import create_investment_data_graph

from src.workflow.state import State, AppointmentData, ClientData, InvestmentData

from src.workflow.agents.data_collection.agent import DataCollector
from src.workflow.agents.data_collection.dependencies import get_data_collector

def create_graph(
    data_collector: DataCollector = Depends(get_data_collector),
    appointments_subgraph = Depends(create_appointments_graph),
    client_data_subgraph = Depends(create_client_data_graph),
    investment_data_subgraph = Depends(create_investment_data_graph)
 ):
    graph = StateGraph(State)
    
    async def data_collection_node(state: State):
        response = await data_collector.interact(state=state)

        return {
            "investment_data": response.investment_data,
            "client_data": response.client_data,
            "appointment_data": response.appointment_data
        }
    
    async def appointments_node(state: State):
        appointments_state = await appointments_subgraph.ainvoke(state["appointment_data"])

        return {"appointment_data": appointments_state}

    async def client_data_node(state: State):
        client_data_state = await client_data_subgraph.ainvoke(state["client_data"])

        return {"client_data": client_data_state}
    
    async def investment_data_node(state: State):
        investment_data_state = await investment_data_subgraph.ainvoke(state["investment_data"])

        return {"investment_data": investment_data_state}
    
    graph.add_node("data_collection", data_collection_node)
    graph.add_node("appointments", appointments_node)
    graph.add_node("client_data", client_data_node)
    graph.add_node("investment_data", investment_data_node)

    graph.add_edge(START, "data_collection")
    graph.add_edge("appointments", END)
    graph.add_edge("client_data", END)
    graph.add_edge("investment_data", END)

    return graph.compile()