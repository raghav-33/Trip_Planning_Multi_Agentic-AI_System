import os
import re
from backend.state import TravelState
from langgraph.types import interrupt
from langchain_core.messages import SystemMessage , AIMessage , HumanMessage , BaseMessage
from backend.config import get_llm
import asyncio

import json

from mcp_tools.mcp_client import (
    tavily_search,
    list_airports,
    list_airlines,
    forecast,
    current_weather
)
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
llm = get_llm()

def _llm_text(system:str , prompt:str) -> str:
    response = llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(content=prompt)
        ]
    )
    return response.content

# Converting Json Response Given by LLM into Python Dictionary , so keys can accessed
def _json_from_llm(text: str) -> dict:
    print("\n========== RAW LLM RESPONSE ==========")
    print(text)
    print("======================================\n")

    start = text.index("{")
    end = text.rindex("}") + 1

    json_text = text[start:end]
    
    # 1. Strip // comments (e.g., // Rs 2 lakh)
    json_text = re.sub(r'//.*', '', json_text)
        
        # 2. Strip /* block comments */ just in case
    json_text = re.sub(r'/\*.*?\*/', '', json_text, flags=re.DOTALL)

    print("\n========== EXTRACTED JSON ==========")
    print(json_text)
    print("====================================\n")

    return json.loads(json_text)

#### Nodes #####

# Supervisor Node
def supervisor_agent(state: TravelState):
    query = state["user_query"]
    
    prompt = f"""
    You are the supervisor of a real-world multi-agent travel planning system.

    Decide which specialist agents are needed for this user request.

    Available agents:
    - flight_agent: use when flights, airports, airlines, routes, or airfare guidance are needed
    - hotel_agent: use when hotels, stays, neighborhoods, or accommodation are needed
    - weather_agent: use when weather, climate, season, packing, or forecast is useful
    - budget_agent: use when budget, affordability, cost, or price constraints are mentioned
    - itinerary_agent: almost always needed to produce the travel plan

    Return ONLY strict JSON with this schema. DO NOT include any comments (like //) inside the JSON block.
    {{
    "selected_agents": ["flight_agent", "hotel_agent", "weather_agent", "budget_agent", "itinerary_agent"],
    "trip_constraints": {{
        "destination": "",
        "origin": "",
        "duration": "",
        "budget": "",
        "travel_style": "",
        "special_preferences": []
    }},
    "reasoning": ""
    }}

    User request:
    {query}
    """

    raw = _llm_text(
        "You route work to specialist agents. Return strict JSON only.",
        prompt

    )

    print("\n========== RAW LLM RESPONSE ==========")
    print(raw)
    print("======================================\n")

    parsed = _json_from_llm(raw)

    print("\n========== PARSED JSON ==========")
    print(json.dumps(parsed, indent=2))
    print("=================================\n")

    print(type(raw))
    print(type(parsed))

    selected = parsed["selected_agents"]

    return {
        "selected_agents": selected,
        "trip_constraints": parsed["trip_constraints"],
        "supervisor_reasoning": parsed["reasoning"],
        "messages": [AIMessage(content="Supervisor created the agent plan.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
    

# Node 1 : Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    constraints = state["trip_constraints"]
    destination = constraints["destination"]

    print("\n========== FLIGHT AGENT INPUT ==========")
    print("Query:", query)
    print("Constraints:", constraints)
    print("========================================\n")

    airports = asyncio.run(list_airports(destination, limit=10))
    airlines = asyncio.run(list_airlines("", limit=10))

    print("\n========== AIRPORT MCP DATA ==========")
    print(airports)
    print("======================================\n")

    print("\n========== AIRLINE MCP DATA ==========")
    print(airlines)
    print("======================================\n")

    prompt = f"""
    Create flight guidance for this trip.

    User request:
    {query}

    Trip constraints:
    {constraints}

    Airport MCP data:
    {str(airports)[:3000]}

    Airline MCP data:
    {str(airlines)[:3000]}

    Include likely departure/arrival airports, relevant airlines,
    estimated duration, fare range, peak season warning,
    and booking advice.
    """

    result = _llm_text(
        "You are a flight planning specialist.",
        prompt,
    )

    print("\n========== FLIGHT AGENT OUTPUT ==========")
    print(result)
    print("=========================================\n")

    return {
        "flight_results": result,
        "messages": [AIMessage(content="Flight agent completed.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


### Node 2
# Node 2 : Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels and areas to stay for: {state['user_query']}"

    print("\n========== HOTEL AGENT INPUT ==========")
    print(query)
    print("=======================================\n")

    result = asyncio.run(tavily_search(query))

    print("\n========== HOTEL SEARCH RESULT ==========")
    print(result)
    print("=========================================\n")

    return {
        "hotel_results": str(result),
        "messages": [AIMessage(content="Hotel agent completed.")],
    }

## Node 3
# Node 3 : wheather Agent
def weather_agent(state: TravelState):
    constraints = state["trip_constraints"]
    city = constraints["destination"]

    print("\n========== WEATHER AGENT INPUT ==========")
    print("City:", city)
    print("=========================================\n")

    weather_data = asyncio.run(current_weather(city))
    forecast_data = asyncio.run(forecast(city))

    print("\n========== CURRENT WEATHER ==========")
    print(weather_data)
    print("=====================================\n")

    print("\n========== WEATHER FORECAST ==========")
    print(forecast_data)
    print("======================================\n")

    result = f"""
    Current weather:
    {weather_data}

    Forecast:
    {forecast_data}
    """

    print("\n========== WEATHER AGENT OUTPUT ==========")
    print(result)
    print("==========================================\n")

    return {
        "weather_results": result,
        "messages": [AIMessage(content="Weather agent completed.")],
    }


## Node 4
## Node 4 : Budget Agent
def budget_agent(state: TravelState):

    print("\n========== BUDGET AGENT INPUT ==========")
    print("Trip Constraints:")
    print(state.get("trip_constraints"))
    print("\nFlight Results:")
    print(state.get("flight_results"))
    print("\nHotel Results:")
    print(state.get("hotel_results"))
    print("\nWeather Results:")
    print(state.get("weather_results"))
    print("=========================================\n")

    prompt = f"""
    Analyze whether this trip plan is realistic for the user's budget.

    User request:
    {state['user_query']}

    Constraints:
    {state.get('trip_constraints', {})}

    Flight results:
    {state.get('flight_results', '')}

    Hotel results:
    {state.get('hotel_results', '')}

    Weather results:
    {state.get('weather_results', '')}

    Return a concise budget assessment with:
    1. estimated cost categories
    2. risk areas
    3. money-saving suggestions
    4. whether the plan seems feasible
    """

    result = _llm_text(
        "You are a practical travel budget analyst.",
        prompt,
    )

    print("\n========== BUDGET AGENT OUTPUT ==========")
    print(result)
    print("=========================================\n")

    return {
        "budget_results": result,
        "messages": [AIMessage(content="Budget agent completed.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

## Node 5
# Node 5 : Itineary Agent

def itinerary_agent(state: TravelState):

    print("\n========== ITINERARY AGENT INPUT ==========")
    print("Trip Constraints:")
    print(state.get("trip_constraints"))

    print("\nFlight Results:")
    print(state.get("flight_results"))

    print("\nHotel Results:")
    print(state.get("hotel_results"))

    print("\nWeather Results:")
    print(state.get("weather_results"))

    print("\nBudget Results:")
    print(state.get("budget_results"))
    print("===========================================\n")

    prompt = f"""
    Create a clear draft travel itinerary.

    User request:
    {state['user_query']}

    Trip constraints:
    {state.get('trip_constraints', {})}

    Flight results:
    {state.get('flight_results', '')}

    Hotel results:
    {state.get('hotel_results', '')}

    Weather results:
    {state.get('weather_results', '')}

    Budget results:
    {state.get('budget_results', '')}

    Make the output structured, practical, and ready for human review.
    """

    result = _llm_text(
        "You are an expert itinerary planner.",
        prompt,
    )

    print("\n========== ITINERARY OUTPUT ==========")
    print(result)
    print("======================================\n")

    approval_request = f"""
    Please review this draft travel plan.

    {result}

    Reply with approval or feedback.
"""

    return {
        "itinerary": result,
        "approval_request": approval_request,
        "messages": [AIMessage(content="Draft itinerary created for human review.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
    
## Node : 6
# Node : Human Approval Agent    
def human_approval_agent(state: TravelState):
    feedback = interrupt(
        {
            "question": "Do you approve this itinerary?",
            "draft_itinerary": state.get("itinerary", ""),
            "approval_request": state.get("approval_request", ""),
            "expected_response": {
                "approved": True,
                "feedback": "Optional feedback for revision",
            },
        }
    )

    approved = feedback["approved"]
    human_feedback = feedback["feedback"]

    return {
        "approved": approved,
        "human_feedback": human_feedback,
        "messages": [AIMessage(content="Human approval step completed.")],
    }


## Node : 7
# Node : Final Response Agent  
'''
def final_response_agent(state: TravelState):

    print("\n========== FINAL AGENT INPUT ==========")
    print("Approved:", state.get("approved"))
    print("Feedback:", state.get("human_feedback"))
    print("=======================================\n")

    if state["approved"]:
        prompt = f"""
        The human approved this draft itinerary.

        Produce the final polished travel plan.

        Draft itinerary:
        {state['itinerary']}

        Budget notes:
        {state['budget_results']}
"""
    else:
        prompt = f"""
        The human did not approve the draft.

        Original user request:
        {state['user_query']}

        Draft itinerary:
        {state['itinerary']}

        Human feedback:
        {state['human_feedback']}

        Budget notes:
        {state['budget_results']}
"""

    result = _llm_text(
        "You produce final user-ready travel plans.",
        prompt,
    )

    print("\n========== FINAL RESPONSE ==========")
    print(result)
    print("====================================\n")

    return {
        "final_response": result,
        "messages": [AIMessage(content=result)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

'''
def final_response_agent(state: TravelState):

    print("\n========== FINAL AGENT INPUT ==========")
    print("Approved:", state.get("approved"))
    print("Feedback:", state.get("human_feedback"))
    print("=======================================\n")

    # Safely extract data using .get() to prevent KeyErrors
    itinerary_data = state.get('itinerary', 'No itinerary generated.')
    budget_data = state.get('budget_results', 'No budget assessment required.')
    user_query = state.get('user_query', 'No query found.')
    human_feedback = state.get('human_feedback', 'None')

    # Use the safe variables in the prompts instead of state['key']
    if state.get("approved"):
        prompt = f"""
        The human approved this draft itinerary.

        Produce the final polished travel plan.

        Draft itinerary:
        {itinerary_data}

        Budget notes:
        {budget_data}
"""
    else:
        prompt = f"""
        The human did not approve the draft.

        Original user request:
        {user_query}

        Draft itinerary:
        {itinerary_data}

        Human feedback:
        {human_feedback}

        Budget notes:
        {budget_data}
"""

    result = _llm_text(
        "You produce final user-ready travel plans.",
        prompt,
    )

    print("\n========== FINAL RESPONSE ==========")
    print(result)
    print("====================================\n")

    return {
        "final_response": result,
        "messages": [AIMessage(content=result)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
