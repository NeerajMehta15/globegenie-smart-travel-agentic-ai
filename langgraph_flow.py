import langgraph as lg
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_groq import ChatGroq
from typing import Dict, List, Any, Annotated
from typing_extensions import TypedDict

from agent import constraint_builder
from agent import extract_requirements
from agent import feedback_handler
from agent import intent_identifier
from agent import planning_agent
from agent import recommendation_node
from agent import super_agent



# Define the state schema using TypedDict
class AgentState(TypedDict):
    user_id: int
    user_query : str
    user_preferrence_1: str
    user_preferrence_2: str
    user_preferrence_3: str

#Create langraph agent state
graph = StateGraph(AgentState)


#add notes
graph.add_node("constraint_builder",constraint_builder)
graph.add_node("extract_requirements",extract_requirements)
graph.add_node("feedback_handler",feedback_handler)
graph.add_node("planning_agent",planning_agent)
graph.add_node("recommendation_nodel",recommendation_node)
graph.add_node("super_agent",super)

#add conditional nodes
    