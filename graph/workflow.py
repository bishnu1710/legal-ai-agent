# @bishnu- legal_ai_agent workflow.py

from langgraph.graph import StateGraph
from typing import TypedDict, List

from agents.parser import parser_agent
from agents.classifier import classifier_agent
from agents.risk_agent import risk_agent
from agents.explanation_agent import explanation_agent
from agents.compliance_agent import compliance_agent
from agents.report_agent import report_agent

#Aggregator node
def aggregator_agent(state):
    # Just passes state forward (ensures all branches complete)
    return state


class AgentState(TypedDict):
    document: str
    clauses: List[str]
    classification: List[str]
    risks: List[str]
    explanations: List[str]
    compliance_issues: List[str]
    final_report: str


def build_graph():
    builder = StateGraph(AgentState)

    # Nodes
    builder.add_node("parser", parser_agent)
    builder.add_node("classifier", classifier_agent)
    builder.add_node("risk", risk_agent)
    builder.add_node("explanation", explanation_agent)
    builder.add_node("compliance", compliance_agent)
    builder.add_node("aggregator", aggregator_agent)  
    builder.add_node("report", report_agent)

    # Entry
    builder.set_entry_point("parser")

    # Flow
    builder.add_edge("parser", "classifier")

    # Parallel branches
    builder.add_edge("classifier", "risk")
    builder.add_edge("classifier", "explanation")
    builder.add_edge("classifier", "compliance")

    # Merge into aggregator
    builder.add_edge("risk", "aggregator")
    builder.add_edge("explanation", "aggregator")
    builder.add_edge("compliance", "aggregator")

    # Final
    builder.add_edge("aggregator", "report")

    return builder.compile()


graph = build_graph()


def run_workflow(document):
    return graph.invoke({"document": document})