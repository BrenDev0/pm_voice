from langgraph.graph import StateGraph, START, END
from src.workflow.state import State


def create_graph():
    graph = StateGraph(State)


    return graph.compile()