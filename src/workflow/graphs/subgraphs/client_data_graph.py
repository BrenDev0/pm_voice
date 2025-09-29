import os
from fastapi import Depends
from langgraph.graph import StateGraph, START, END
from src.workflow.state import ClientData


def create_client_data_graph():
    graph = StateGraph(ClientData)

    def router(state: ClientData):
        pass

    return graph.compile()