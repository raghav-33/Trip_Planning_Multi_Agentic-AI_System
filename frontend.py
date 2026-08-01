
import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from backend.graph import app

# -------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="centered",
)

st.title("✈️ AI Trip Planner")
st.caption("Plan your entire trip using multiple AI agents")

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.header("Session")

    user_id = st.text_input(
        "User ID",
        value="demo_user"
    )

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

    if st.button("New Conversation"):
        st.session_state.thread_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

        st.session_state.pop("latest_result", None)
        st.session_state.pop("waiting_for_approval", None)

    st.write(st.session_state.thread_id)

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# -------------------------------------------------------
# User Input
# -------------------------------------------------------

query = st.text_area(
    "Describe your trip",
    placeholder="Example: Plan a 4-day Goa trip from Amritsar under Rs 20,000",
    height=120,
)

# -------------------------------------------------------
# Generate Draft
# -------------------------------------------------------

if st.button("Generate Travel Plan", use_container_width=True):

    if not query.strip():
        st.warning("Enter your travel request.")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    latest_state = None

    progress_map = {
        "supervisor": 10,
        "flight_agent": 25,
        "hotel_agent": 45,
        "weather_agent": 60,
        "budget_agent": 75,
        "itinerary_agent": 95,
        "human_approval": 100,
    }

    status_text = {
        "supervisor": "🧠 Supervisor analysing request...",
        "flight_agent": "✈️ Finding flights...",
        "hotel_agent": "🏨 Searching hotels...",
        "weather_agent": "🌤 Fetching weather...",
        "budget_agent": "💰 Calculating budget...",
        "itinerary_agent": "📝 Creating itinerary...",
        "human_approval": "⏸ Waiting for approval...",
        "final_response": "✅ Finalizing travel plan..."
    }

    try:

        for chunk in app.stream(

            {
                "messages": [HumanMessage(content=query)],
                "user_id": user_id,
                "user_query": query,
                "flight_results": "",
                "hotel_results": "",
                "weather_results": "",
                "budget_results": "",
                "itinerary": "",
                "final_response": "",
                "llm_calls": 0,
            },

            config=config,
            stream_mode="updates",

        ):

            latest_state = chunk

            node = list(chunk.keys())[0]

            progress.progress(progress_map.get(node, 0))

            status.info(status_text.get(node, node))

        progress.empty()

        status.success("Draft itinerary generated!")

        st.session_state.latest_result = latest_state

        st.session_state.waiting_for_approval = "__interrupt__" in latest_state

    except Exception as e:

        progress.empty()

        status.empty()

        st.error(e)

# -------------------------------------------------------
# Draft Itinerary
# -------------------------------------------------------

result = st.session_state.get("latest_result")

if result:

    st.divider()

    st.subheader("📝 Draft Itinerary")

    if "__interrupt__" in result:

        itinerary = result["__interrupt__"][0].value["draft_itinerary"]

    else:

        itinerary = result.get("itinerary", "")

    st.markdown(itinerary)

# -------------------------------------------------------
# Human Approval
# -------------------------------------------------------

if st.session_state.get("waiting_for_approval"):

    st.divider()

    st.subheader("Human Approval")

    approved = st.radio(

        "Approve itinerary?",

        ["Approve", "Reject"],

        horizontal=True,

    )

    feedback = ""

    if approved == "Reject":

        feedback = st.text_area(

            "Feedback",

            placeholder="Tell the AI what to improve..."

        )

    if st.button("Submit Decision", use_container_width=True):

        progress = st.progress(0)

        status = st.empty()

        try:

            progress.progress(50)

            status.info("Updating itinerary...")

            final_state = None

            for chunk in app.stream(

                Command(

                    resume={

                        "approved": approved == "Approve",

                        "feedback": feedback,

                    }

                ),

                config=config,

                stream_mode="updates",

            ):

                final_state = chunk

            progress.progress(100)

            status.success("Travel plan ready!")

            st.session_state.latest_result = final_state

            st.session_state.waiting_for_approval = False

            st.rerun()

        except Exception as e:

            st.error(e)

# -------------------------------------------------------
# Final Response
# -------------------------------------------------------

final_chunk = st.session_state.get("latest_result")

if final_chunk:
    
    # 1. Get the name of the node that just finished (e.g., 'human_approval' or 'final_response')
    node_name = list(final_chunk.keys())[0]
    
    # 2. Extract the actual state update dictionary from inside that node
    state_update = final_chunk[node_name]

    # 3. Check if the final string exists inside the state and render it
    if isinstance(state_update, dict) and "final_response" in state_update:

        st.divider()

        st.subheader("🎉 Final Travel Plan")

        st.markdown(state_update["final_response"])