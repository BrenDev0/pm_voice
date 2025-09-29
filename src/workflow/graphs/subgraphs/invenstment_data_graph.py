from langgraph.graph import StateGraph, START, END
from src.workflow.state import InvestmentData

def create_investment_data_graph():
    graph = StateGraph(InvestmentData)

    def router(state: InvestmentData):
        pass

    return graph.compile()