import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


import json
from statistics import mean

from langsmith import Client
from langgraph.types import Command

from backend.graph import app

from Evaluation.evaluators import (
    evaluate_supervisor,
    evaluate_flight,
    evaluate_hotel,
    evaluate_weather,
    evaluate_budget,
    evaluate_itinerary,
    evaluate_final_response,
)


# --------------------------------------------------------
# LangSmith
# --------------------------------------------------------

client = Client()

DATASET_NAME = "MultiAgent_TravelPlanner_Evaluation"


# --------------------------------------------------------
# Run Graph
# --------------------------------------------------------

def run_graph(query: str):
    state = {
        "messages": [],
        "user_id": "evaluation",
        "user_query": query,
        "llm_calls": 0,
    }
    config = {"configurable": {"thread_id": f"eval-{abs(hash(query))}"}}

    # 1. Run until the human interrupt
    app.invoke(state, config=config)
    
    # 2. Automatically approve it so the graph finishes
    result = app.invoke(
        Command(resume={"approved": True, "feedback": "Looks good!"}),
        config=config
    )
    return result


# --------------------------------------------------------
# Main Evaluation
# --------------------------------------------------------

def evaluate():

    dataset = client.read_dataset(dataset_name=DATASET_NAME)

    examples = list(
        client.list_examples(
            dataset_id=dataset.id
        )
    )[:9]

    all_results = []

    supervisor_scores = []
    flight_scores = []
    hotel_scores = []
    weather_scores = []
    budget_scores = []
    itinerary_scores = []
    final_scores = []

    for i, example in enumerate(examples, start=1):

        print("=" * 70)
        print(f"Example {i}")
        print("=" * 70)

        query = example.inputs["query"]

        expected = example.outputs

        print(query)

        graph_state = run_graph(query)

        prediction = {
            "selected_agents": graph_state.get(
                "selected_agents", []
            ),
            "trip_constraints": graph_state.get(
                "trip_constraints", {}
            ),
        }

        result = {
            "query": query
        }

        # ------------------------------------------------
        # Supervisor
        # ------------------------------------------------

        supervisor_eval = evaluate_supervisor(
            query=query,
            expected=expected,
            prediction=prediction,
        )

        result["supervisor"] = supervisor_eval
        supervisor_scores.append(
            supervisor_eval["overall_score"]
        )

        selected = graph_state.get(
            "selected_agents", []
        )

        constraints = graph_state.get(
            "trip_constraints", {}
        )

        # ------------------------------------------------
        # Flight
        # ------------------------------------------------

        if "flight_agent" in selected:

            score = evaluate_flight(
                query=query,
                constraints=constraints,
                output=graph_state.get(
                    "flight_results",
                    "",
                ),
            )

            result["flight"] = score
            flight_scores.append(
                score["overall_score"]
            )

        # ------------------------------------------------
        # Hotel
        # ------------------------------------------------

        if "hotel_agent" in selected:

            score = evaluate_hotel(
                query=query,
                output=graph_state.get(
                    "hotel_results",
                    "",
                ),
            )

            result["hotel"] = score
            hotel_scores.append(
                score["overall_score"]
            )

        # ------------------------------------------------
        # Weather
        # ------------------------------------------------

        if "weather_agent" in selected:

            score = evaluate_weather(
                destination=constraints.get(
                    "destination",
                    "",
                ),
                output=graph_state.get(
                    "weather_results",
                    "",
                ),
            )

            result["weather"] = score
            weather_scores.append(
                score["overall_score"]
            )

        # ------------------------------------------------
        # Budget
        # ------------------------------------------------

        if "budget_agent" in selected:

            score = evaluate_budget(
                query=query,
                constraints=constraints,
                output=graph_state.get(
                    "budget_results",
                    "",
                ),
            )

            result["budget"] = score
            budget_scores.append(
                score["overall_score"]
            )

        # ------------------------------------------------
        # Itinerary
        # ------------------------------------------------

        itinerary_score = evaluate_itinerary(
            query=query,
            itinerary=graph_state.get(
                "itinerary",
                "",
            ),
        )

        result["itinerary"] = itinerary_score

        itinerary_scores.append(
            itinerary_score["overall_score"]
        )

        # ------------------------------------------------
        # Final Response
        # ------------------------------------------------

        final_score = evaluate_final_response(
            query=query,
            response=graph_state.get(
                "final_response",
                "",
            ),
        )

        result["final_response"] = final_score

        final_scores.append(
            final_score["overall_score"]
        )

        all_results.append(result)

    # ----------------------------------------------------
    # Overall Metrics
    # ----------------------------------------------------

    summary = {
        "Supervisor": round(mean(supervisor_scores), 2),

        "Flight": round(mean(flight_scores), 2)
        if flight_scores else None,

        "Hotel": round(mean(hotel_scores), 2)
        if hotel_scores else None,

        "Weather": round(mean(weather_scores), 2)
        if weather_scores else None,

        "Budget": round(mean(budget_scores), 2)
        if budget_scores else None,

        "Itinerary": round(mean(itinerary_scores), 2),

        "Final Response": round(mean(final_scores), 2),
    }

    report = {
        "summary": summary,
        "examples": all_results,
    }

    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nEvaluation Complete")
    print(json.dumps(summary, indent=4))


if __name__ == "__main__":
    evaluate()