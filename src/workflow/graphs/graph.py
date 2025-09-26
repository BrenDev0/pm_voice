import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END

from src.workflow.state import State

from src.workflow.agents.data_collection.agent import DataCollector
from src.workflow.agents.data_collection.dependencies import get_data_collector

def create_graph(
    data_collector: DataCollector = Depends(get_data_collector)
):
    graph = StateGraph(State)
    
    async def data_collection_node(state: State):
        response = await data_collector.interact(state=state)

        return {
            "invenstment_data": response.investment_data,
            "client_data": response.client_data,
            "appointment_data": response.appointment_data
        }
    
    graph.add_node("data_collection", data_collection_node)

    graph.add_edge(START, "data_collector")

    return graph.compile()