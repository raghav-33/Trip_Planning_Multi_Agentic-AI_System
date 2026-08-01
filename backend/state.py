from langgraph.graph import StateGraph,START,END
from typing import TypedDict , Annotated , Any
from langchain_core.messages import BaseMessage
import operator

class TravelState(TypedDict):
    messages : Annotated[list[BaseMessage],operator.add]
    user_id : str
    user_query : str
    
    trip_constraints: dict[str, Any]
    selected_agents: list[str]
    supervisor_reasoning: str # give Reason why selected particular agent
    
    flight_results: str
    hotel_results: str
    itinerary: str
    weather_results: str
    budget_results: str
   
    approval_request: str
    human_feedback: str
    approved: bool

    final_response: str
    llm_calls: int
    
