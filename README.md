# ✈️ Multi-Agent AI Travel Planner

An AI-powered travel planning system that uses multiple specialized agents to create personalized travel itineraries. Users can review the itinerary, provide feedback, and approve changes through a Human-in-the-Loop (HITL) workflow before the final plan is generated.

## Overview

The Multi-Agent AI Travel Planner leverages **LangGraph** to orchestrate a team of specialized AI agents. By utilizing the **Model Context Protocol (MCP)**, these agents securely interact with external APIs to fetch real-time flight, weather, and general travel data. The system persists state across sessions using **PostgreSQL**, allowing users to interrupt the AI's workflow, review draft itineraries, and provide feedback before finalization.

## Problem Statement

Travel planning involves more than just generating an itinerary. It requires up-to-date flight information, weather forecasts, accommodation options, and budget planning. Traditional LLMs can struggle with real-time data and multi-step decision-making.Traditional LLMs hallucinate real-time data and struggle with complex, multi-step constraints. To overcome this, the system uses multiple AI agents that collaborate and retrieve live information from external APIs before generating the final itinerary. .

## Solution

The system uses a multi-agent architecture where each AI agent focuses on a specific responsibility instead of trying to solve the entire problem alone. A Supervisor agent coordinates the workflow and delegates tasks to specialized agents for flights, weather, budgeting, and itinerary planning. The agents access real-time data through MCP tools, and the application's persistent state allows users to review drafts, provide feedback, and refine the itinerary without restarting the planning process.

## Features

- **Multi-Agent Orchestration**: Dynamic task routing via a LangGraph Supervisor to Flight, Hotel, Weather, Budget, and Itinerary sub-agents.
- **Model Context Protocol (MCP)**: Standardized, secure tool execution running as isolated local sub-processes (stdio) for external API communication.
- **Human-in-the-Loop (HITL)**: Thread-level execution pausing allowing users to approve or reject draft itineraries with custom feedback.
- **Persistent Memory**: PostgreSQL-backed checkpointer (`langgraph-checkpoint-postgres`) saves conversational and agent state across sessions.
- **Real-Time Data Streaming**: Frontend UI updates asynchronously as individual agents complete their tasks.

## Architecture

```mermaid
graph TD
    UI[Streamlit Frontend] <--> |Session State & Stream| LG[LangGraph Orchestrator]

    subgraph AI Backend
        LG <--> Sup[Supervisor Agent]
        Sup --> FA[Flight Agent]
        Sup --> HA[Hotel Agent]
        Sup --> WA[Weather Agent]
        Sup --> BA[Budget Agent]
        Sup --> IA[Itinerary Agent]
    end

    subgraph Persistent Storage
        LG <--> |State Checkpointing| DB[(PostgreSQL)]
    end

    subgraph External Tools via MCP
        FA <--> |stdio / runner script| Aviation[AviationStack MCP]
        WA <--> |stdio| Weather[OpenWeather MCP]
        IA <--> |HTTP| Tavily[Tavily Search MCP]
    end
```

## Folder Structure

```
Trip_Planning_Multi_Agentic_AI_System/
├── frontend.py                 # Streamlit UI, Session config, and App streaming logic
├── requirements.txt            # Project dependencies (LangGraph, MCP, Streamlit, etc.)
├── .env                        # Environment variables (Ignored in version control)
├── backend/
│   ├── graph.py                # LangGraph state definitions, node routing, and compiled app
│   └── agents.py               # Individual agent logic (Supervisor, Flight, Hotel, etc.)
└── mcp_tools/                  # Model Context Protocol configurations
    ├── mcp_client.py           # MultiServerMCPClient configuration and tool definitions
    ├── weather_mcp_server.py   # OpenWeather MCP server implementation
    ├── aviation_runner.py      # Custom Python runner to force pathing for aviation module
    └── aviationstack-mcp/      # Local standard input/output MCP server for flights
```

## Tech Stack

| Category | Technology |
|---|---|
| Frontend | Streamlit |
| Backend Orchestration | Python 3.11, LangGraph, LangChain |
| LLM Integration | langchain-groq |
| State Persistence | PostgreSQL, psycopg-pool, langgraph-checkpoint-postgres |
| Tool Protocol | mcp==1.28.1, langchain-mcp-adapters |
| Deployment | Render |

## AI Pipeline

The AI logic operates as a cyclic state machine utilizing LangGraph:

- **State Management**: Passes a typed dictionary containing `user_query`, `flight_results`, `hotel_results`, `weather_results`, `budget_results`, `itinerary`, and `final_response`.
- **Supervisor Agent**: Acts as the router. Evaluates the current state and determines which worker agent should execute next.
- **Worker Agents**:
  - **Flight Agent**: Connects to `aviationstack-mcp`.
  - **Weather Agent**: Connects to `weather_mcp_server.py`.
  - **Hotel/Budget Agents**: Analyzes context to structure budget and accommodation data.
  - **Itinerary Agent**: Synthesizes the aggregated state data into a Markdown draft.

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL running locally or accessible via cloud.

### Step-by-Step

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Trip_Planning_Multi_Agentic_AI_System.git
cd Trip_Planning_Multi_Agentic_AI_System
```

2. Set up the virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory:

| Variable | Purpose | Example |
|---|---|---|
| `TAVILY_API_KEY` | Authentication for Tavily Search MCP | `tvly-xxxxxxxxxxxx` |
| `AVIATIONSTACK_API_KEY` | Real-time flight data API key | `axxxxxxxxxxxxxx` |
| `OPENWEATHER_API_KEY` | Real-time weather forecasting | `oxxxxxxxxxxxxxx` |
| `GROQ_API_KEY` | Authentication for the core LLM | `gsk_xxxxxxxxxxxxx` |
| `DATABASE_URL` | PostgreSQL connection for LangGraph checkpointer | `postgresql://user:pass@localhost:5432/db` |

## Usage

1. Start the Streamlit application locally:

```bash
streamlit run frontend.py
```

2. Enter a unique User ID in the sidebar to maintain session state.
3. Type a travel query (e.g., "Plan a 4-day Goa trip from Amritsar under Rs 20,000").
4. Monitor the progress bar as the Supervisor routes tasks to agents.
5. Review the Draft Itinerary.
6. Click **Approve** to finalize, or **Reject** and provide feedback to force the AI to regenerate the plan based on your constraints.

## API Documentation

This application is a monolithic frontend/backend hybrid and does not expose standard REST API endpoints to the public. However, the internal `mcp_client.py` orchestrates the following external tools:

| Tool Name | Purpose | Parameters |
|---|---|---|
| `tavily_search` | General web queries | `query` |
| `list_airports` | AviationStack airport lookup | `search`, `limit`, `offset` |
| `list_airlines` | AviationStack airline lookup | `search`, `limit`, `offset` |
| `get_current_weather` | OpenWeather real-time data | `city` |
| `get_forecast` | OpenWeather future forecasting | `city` |

## Evaluation

The system has been evaluated for domain accuracy and orchestration efficiency.

| Metric / Agent | Score (Out of 5.0) |
|---|---|
| Itinerary Generation | 4.40 |
| Flight Routing | 4.37 |
| Final Response Coherence | 4.13 |
| Budget Accuracy | 3.98 |
| Weather Accuracy | 3.93 |
| Hotel Sourcing | 3.89 |
| Supervisor (Strict Routing Threshold) | 4.38 |

## Performance

- **Latency (p50)**: 8.3 seconds
- **Latency (p99)**: 69.9 seconds
- **Optimizations**: The application utilizes an `_tools_cache` global variable in `mcp_client.py` to prevent redundant loading and initialization of MCP servers across asynchronous LLM calls.



## Deployment

This project is configured for cloud deployment on Render.

- **Port Binding**: Streamlit binds to Render's default port 10000.
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0`

## Live | Deployed Project Link
```bash
https://trip-planning-multi-agentic-ai-system.onrender.com
```


## Future Improvements

- Replace local stdio MCP execution with external REST or SSE-based MCP servers to fully decouple the AI backend from environment-specific pathing issues.
- Implement LangSmith tracing for granular observability into the Supervisor's routing logic.
- Add multi-modal outputs (e.g., generating maps or hotel images) to the Streamlit UI.

## License

MIT License

## Author

Raghav
