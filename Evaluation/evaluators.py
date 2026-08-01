from Evaluation.judge import judge
from Evaluation.prompts import (
    SUPERVISOR_JUDGE_PROMPT,
    FLIGHT_JUDGE_PROMPT,
    HOTEL_JUDGE_PROMPT,
    WEATHER_JUDGE_PROMPT,
    BUDGET_JUDGE_PROMPT,
    ITINERARY_JUDGE_PROMPT,
    FINAL_RESPONSE_JUDGE_PROMPT,
)


# ---------------------------------------------------
# Supervisor Evaluation
# ---------------------------------------------------

def evaluate_supervisor(
    query,
    expected,
    prediction,
):
    return judge(
        SUPERVISOR_JUDGE_PROMPT,
        query=query,
        expected_agents=expected["selected_agents"],
        predicted_agents=prediction["selected_agents"],
        expected_constraints=expected["trip_constraints"],
        predicted_constraints=prediction["trip_constraints"],
    )


# ---------------------------------------------------
# Flight Agent
# ---------------------------------------------------

def evaluate_flight(
    query,
    constraints,
    output,
):
    return judge(
        FLIGHT_JUDGE_PROMPT,
        query=query,
        constraints=constraints,
        output=output,
    )


# ---------------------------------------------------
# Hotel Agent
# ---------------------------------------------------

def evaluate_hotel(
    query,
    output,
):
    return judge(
        HOTEL_JUDGE_PROMPT,
        query=query,
        output=output,
    )


# ---------------------------------------------------
# Weather Agent
# ---------------------------------------------------

def evaluate_weather(
    destination,
    output,
):
    return judge(
        WEATHER_JUDGE_PROMPT,
        destination=destination,
        output=output,
    )


# ---------------------------------------------------
# Budget Agent
# ---------------------------------------------------

def evaluate_budget(
    query,
    constraints,
    output,
):
    return judge(
        BUDGET_JUDGE_PROMPT,
        query=query,
        constraints=constraints,
        output=output,
    )


# ---------------------------------------------------
# Itinerary Agent
# ---------------------------------------------------

def evaluate_itinerary(
    query,
    itinerary,
):
    return judge(
        ITINERARY_JUDGE_PROMPT,
        query=query,
        itinerary=itinerary,
    )


# ---------------------------------------------------
# Final Response
# ---------------------------------------------------

def evaluate_final_response(
    query,
    response,
):
    return judge(
        FINAL_RESPONSE_JUDGE_PROMPT,
        query=query,
        response=response,
    )