import streamlit as st
import asyncio
import uuid
import nest_asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Apply nest_asyncio to allow asyncio.run inside Streamlit's own event loop
nest_asyncio.apply()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Travel Concierge ✈️",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 40%, #0a1628 70%, #0f1923 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f35 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(180, 155, 100, 0.2);
}

[data-testid="stSidebar"] * {
    color: #d4c5a0 !important;
}

/* ── Sidebar title ── */
.sidebar-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    color: #c9a84c !important;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}

.sidebar-subtitle {
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(180, 155, 100, 0.6) !important;
    margin-bottom: 1.5rem;
}

/* ── Divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 1rem 0;
}

/* ── Agent pills ── */
.agent-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 2px;
    border: 1px solid;
}
.pill-main   { background: rgba(201,168,76,0.15); border-color: rgba(201,168,76,0.5); color: #c9a84c !important; }
.pill-insp   { background: rgba(100,180,200,0.12); border-color: rgba(100,180,200,0.4); color: #7ac8d8 !important; }
.pill-news   { background: rgba(180,120,200,0.12); border-color: rgba(180,120,200,0.4); color: #c87fd8 !important; }
.pill-places { background: rgba(100,200,140,0.12); border-color: rgba(100,200,140,0.4); color: #6dc89a !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(180,155,100,0.1) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
    padding: 0.75rem 1rem !important;
    backdrop-filter: blur(8px);
}

/* User message accent */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]) {
    transition: border-color 0.2s;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: rgba(13, 31, 53, 0.9) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    border-radius: 12px !important;
    color: #e8dfc8 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(201,168,76,0.7) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.1) !important;
}

/* ── Main header ── */
.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
}

.main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: #c9a84c;
    letter-spacing: 0.08em;
    margin: 0;
}

.main-tagline {
    font-size: 0.8rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(180,155,100,0.5);
    margin-top: 0.3rem;
}

/* ── Welcome card ── */
.welcome-card {
    background: rgba(201,168,76,0.06);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0 2rem;
    text-align: center;
}

.welcome-card p {
    color: rgba(212,197,160,0.8);
    font-size: 0.92rem;
    line-height: 1.7;
    margin: 0;
}

/* ── Suggestion chips ── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 1rem;
}

.chip {
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.8rem;
    color: #c9a84c;
    cursor: pointer;
    transition: all 0.2s;
}

.chip:hover {
    background: rgba(201,168,76,0.2);
}

/* ── Thinking spinner ── */
.thinking-box {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.75rem 1rem;
    background: rgba(201,168,76,0.06);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    color: rgba(201,168,76,0.8);
    letter-spacing: 0.05em;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(201,168,76,0.08)) !important;
    border: 1px solid rgba(201,168,76,0.4) !important;
    color: #c9a84c !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(201,168,76,0.25), rgba(201,168,76,0.15)) !important;
    border-color: rgba(201,168,76,0.7) !important;
    box-shadow: 0 0 12px rgba(201,168,76,0.15) !important;
}

/* ── Message text ── */
.stMarkdown p, .stMarkdown li {
    color: #d4c5a0 !important;
    line-height: 1.75;
}

.stMarkdown strong {
    color: #c9a84c !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,0.3); border-radius: 2px; }

/* ── Session info ── */
.session-info {
    font-size: 0.68rem;
    color: rgba(180,155,100,0.35) !important;
    letter-spacing: 0.08em;
    font-family: monospace;
}
</style>
""", unsafe_allow_html=True)


# ── Agent import (lazy, cached) ────────────────────────────────────────────────
@st.cache_resource
def load_agent():
    """Load the root agent once and cache it."""
    from travel_planner.agent import root_agent
    return root_agent


@st.cache_resource
def get_session_service():
    return InMemorySessionService()


# ── ADK runner (cached per session_id) ────────────────────────────────────────
def get_runner(session_id: str):
    """Create or retrieve a Runner for the given session."""
    if "runner" not in st.session_state:
        agent = load_agent()
        session_service = get_session_service()

        # Create the ADK session
        asyncio.run(
            session_service.create_session(
                app_name="travel_planner",
                user_id="streamlit_user",
                session_id=session_id,
            )
        )

        st.session_state.runner = Runner(
            agent=agent,
            app_name="travel_planner",
            session_service=session_service,
        )

    return st.session_state.runner


# ── Core: send message to agent ───────────────────────────────────────────────
async def _ask_agent_async(runner: Runner, session_id: str, user_message: str) -> str:
    """Send a message and collect the full response text."""
    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    full_response = []

    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session_id,
        new_message=content,
    ):
        # Capture final agent text responses
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        full_response.append(part.text)

    return "\n\n".join(full_response) if full_response else "I couldn't generate a response. Please try again."


def ask_agent(runner: Runner, session_id: str, user_message: str) -> str:
    return asyncio.run(_ask_agent_async(runner, session_id, user_message))


# ── Session state init ─────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "trip_count" not in st.session_state:
    st.session_state.trip_count = 0


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">✈ Travel<br>Concierge</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Powered by Multi-Agent AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown("**Active Agents**")
    st.markdown("""
    <div style="margin: 0.5rem 0 1rem;">
        <span class="agent-pill pill-main">🧭 Travel Planner</span>
        <span class="agent-pill pill-insp">💡 Inspiration</span>
        <span class="agent-pill pill-news">📰 News</span>
        <span class="agent-pill pill-places">📍 Places</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown("**Capabilities**")
    capabilities = [
        "🌍 Destination discovery",
        "📰 Travel news & events",
        "📍 Nearby places & hotels",
        "🏛️ Attractions & activities",
        "🍽️ Restaurants & cafes",
    ]
    for cap in capabilities:
        st.markdown(f"<small style='color: rgba(212,197,160,0.7)'>{cap}</small>", unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # New session button
    if st.button("✦ Start New Journey"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        if "runner" in st.session_state:
            del st.session_state["runner"]
        st.rerun()

    # Session info
    sid_short = st.session_state.session_id[:8]
    st.markdown(f'<div class="session-info" style="margin-top:1rem">Session: {sid_short}...</div>', unsafe_allow_html=True)
    msg_count = len(st.session_state.messages)
    st.markdown(f'<div class="session-info">Messages: {msg_count}</div>', unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-title">Where to next?</div>
    <div class="main-tagline">Your AI-powered travel concierge</div>
</div>
""", unsafe_allow_html=True)

# Welcome card (only when no messages yet)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <p>
            Tell me your dream destination — or let me inspire you.<br>
            I'll find the best places, latest travel news, nearby hotels, cafes & hidden gems using a team of specialized AI agents.
        </p>
        <div class="chip-row">
            <span class="chip">🗼 Plan a Paris trip</span>
            <span class="chip">🏝️ Beach destinations in Asia</span>
            <span class="chip">🏔️ Adventure travel ideas</span>
            <span class="chip">🍜 Hotels near Shibuya crossing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌍" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me about any destination, hotel, event or travel idea…")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Get runner
    runner = get_runner(st.session_state.session_id)

    # Show thinking state + get response
    with st.chat_message("assistant", avatar="🌍"):
        with st.spinner("✦ Your concierge is consulting the agents…"):
            response = ask_agent(runner, st.session_state.session_id, user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()