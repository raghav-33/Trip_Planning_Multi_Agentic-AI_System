SCORING_RUBRIC = """
Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.
"""

SUPERVISOR_JUDGE_PROMPT = """
You are evaluating the Supervisor Agent of a Multi-Agent Travel Planner.

USER QUERY
----------
{query}

EXPECTED SELECTED AGENTS
------------------------
{expected_agents}

PREDICTED SELECTED AGENTS
-------------------------
{predicted_agents}

EXPECTED TRIP CONSTRAINTS
-------------------------
{expected_constraints}

PREDICTED TRIP CONSTRAINTS
--------------------------
{predicted_constraints}

Evaluate:
1. Agent Selection Correctness (Did it pick the exact expected agents?)
2. Constraint Extraction Accuracy (Did it extract the destination, budget, etc. correctly?)
3. Missing Important Information
4. Unnecessary Agents
5. Overall Routing Quality

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

FLIGHT_JUDGE_PROMPT = """
You are evaluating the Flight Agent.

USER QUERY
----------
{query}

TRIP CONSTRAINTS
----------------
{constraints}

FLIGHT AGENT OUTPUT
-------------------
{output}

Evaluate:
1. Did it answer the flight request?
2. Did it respect trip constraints (budget, origin, destination)?
3. Are airport suggestions relevant?
4. Are airline suggestions reasonable?
5. Is booking advice useful?

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

HOTEL_JUDGE_PROMPT = """
You are evaluating the Hotel Agent.

USER QUERY
----------
{query}

HOTEL AGENT OUTPUT
------------------
{output}

Evaluate:
1. Recommended suitable hotels based on the prompt.
2. Suggested good locations/neighborhoods.
3. Useful accommodation advice.
4. Relevance to any stated travel style (e.g., luxury vs. budget).
5. Overall quality.

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

WEATHER_JUDGE_PROMPT = """
You are evaluating the Weather Agent.

Destination
-----------
{destination}

Weather Output
--------------
{output}

Evaluate:
1. Weather information quality (is it clear and readable?)
2. Forecast usefulness (is it actionable?)
3. Travel advice based on weather.
4. Packing suggestions.
5. Overall usefulness.

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

BUDGET_JUDGE_PROMPT = """
You are evaluating the Budget Agent.

User Query
----------
{query}

Trip Constraints
----------------
{constraints}

Budget Output
-------------
{output}

Evaluate:
1. Budget feasibility (Did it correctly assess if the trip is affordable?)
2. Cost estimation accuracy based on context.
3. Money saving suggestions.
4. Practicality of the advice.
5. Overall usefulness.

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

ITINERARY_JUDGE_PROMPT = """
You are evaluating the Itinerary Agent.

USER QUERY
----------
{query}

ITINERARY
---------
{itinerary}

Evaluate:
1. Trip completeness (Does it cover the whole requested duration?)
2. Day-wise planning (Is there a logical flow to the days?)
3. Practicality (Are the activities realistic for a human to do?)
4. Readability (Is the formatting clean and professional?)
5. Overall quality.

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""

FINAL_RESPONSE_JUDGE_PROMPT = """
You are evaluating the FINAL travel plan.

USER QUERY
----------
{query}

FINAL RESPONSE
--------------
{response}

Evaluate:
1. User satisfaction (Would a real user be happy with this plan?)
2. Completeness (Does it synthesize flights, hotels, weather, and budget into one cohesive plan?)
3. Correctness (Are there any glaring contradictions?)
4. Practicality.
5. Overall quality.

Score from 1 to 5 using this exact scale:
1: Completely wrong, hallucinates, or missing entirely.
2: Poor quality, ignores major constraints, or highly impractical.
3: Acceptable, answers the prompt but has minor errors or lacks detail.
4: Good, follows all constraints and is useful, but could be slightly more polished.
5: Perfect, highly practical, accurate, and exceeds expectations.

Return ONLY JSON matching this exact structure:
{{
    "task_completion": 0,
    "accuracy": 0,
    "relevance": 0,
    "reasoning": 0,
    "overall_score": 0,
    "feedback": "brief explanation of your scores"
}}
"""