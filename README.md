# ✈️ Travel Planner — Multi-Agent AI System

A conversational travel concierge built with **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash**. It uses a hierarchy of specialized AI agents to help users discover destinations, find nearby places, and get the latest travel news — all through a natural chat interface.

---

## 🧠 Architecture

```
root_agent  (travel_planner_main)
    └── travel_inspiration_agent
            ├── news_agent        →  google_search_grounding tool
            └── places_agent      →  location_search_tool (OpenStreetMap)
```

| Agent | Role |
|---|---|
| `travel_planner_main` | Orchestrator — routes user queries to sub-agents |
| `travel_inspiration_agent` | Helps users discover destinations & activities |
| `news_agent` | Fetches current travel events & news via Google Search |
| `places_agent` | Finds nearby hotels, cafes, restaurants via OpenStreetMap |

---

## 🗂️ Project Structure

```
travel_planner_with_adk/
├── travel_planner/
│   ├── __init__.py
│   ├── agent.py               # Root agent definition
│   ├── supporting_agents.py   # Sub-agents: inspiration, news, places
│   └── tools.py               # google_search_grounding, location_search_tool
├── main.py                    # Optional: CLI entry point
├── Streamlitapp.py            # Streamlit chat UI
├── .env                       # API keys (not committed)
├── pyproject.toml             # Project dependencies (uv)
├── requirements.txt           # Pip-compatible dependency list
└── uv.lock                    # Locked dependency versions
```

---

## 🚀 Getting Started

<img width="2559" height="1339" alt="1" src="https://github.com/user-attachments/assets/4d013e97-57f7-4c08-baf8-f31c1a5a2ebe" />

<img width="2559" height="1335" alt="2" src="https://github.com/user-attachments/assets/783ca6db-ae61-4f46-bded-00375baf2c02" />

<img width="2557" height="1333" alt="3" src="https://github.com/user-attachments/assets/0d071007-a074-4641-952b-7c23353ee078" />

<img width="2559" height="1330" alt="4" src="https://github.com/user-attachments/assets/5cbcce48-d8ae-4bed-92c8-30ed94953eb9" />

<img width="2559" height="1339" alt="5" src="https://github.com/user-attachments/assets/9b1328a6-ad99-4169-8716-9e14483f42f6" />

<img width="2557" height="1336" alt="6" src="https://github.com/user-attachments/assets/2d5593aa-e2f8-4974-936f-7c610cc2f757" />


### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- A Google API Key with Gemini access

### 1. Clone the repository

```bash
git clone https://github.com/your-username/travel-planner-adk.git
cd travel-planner-adk
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the app

**Option A — Streamlit UI (recommended)**
```bash
uv run streamlit run Streamlitapp.py
```
Opens at: `http://localhost:8501`

**Option B — ADK built-in web UI**
```bash
uv run adk web
```

---

## 💬 Example Queries

| Query | Agents Triggered |
|---|---|
| `Plan a 7-day trip to Japan` | Inspiration → News + Places |
| `Find hotels near Eiffel Tower` | Inspiration → Places |
| `Latest travel news in Bali` | Inspiration → News |
| `Restaurants near Colosseum Rome` | Inspiration → Places |
| `Suggest a beach destination in Asia` | Inspiration |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Google ADK](https://google.github.io/adk-docs/) | Multi-agent orchestration framework |
| Gemini 2.5 Flash | LLM powering all agents |
| Google Search Grounding | Real-time web search for news agent |
| OpenStreetMap / Overpass API | Free location & places search |
| Streamlit | Chat frontend UI |
| geopy | Geocoding location strings to coordinates |
| uv | Fast Python package & project manager |
| nest-asyncio | Async compatibility for Streamlit + ADK |

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | ✅ Yes | Google Gemini API key |

---

## 📦 Dependencies

Key packages (see `pyproject.toml` for full list):

```
google-adk
google-generativeai
streamlit
geopy
requests
nest-asyncio
python-dotenv
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Google ADK](https://google.github.io/adk-docs/) for the multi-agent framework
- [OpenStreetMap](https://www.openstreetmap.org/) & [Overpass API](https://overpass-api.de/) for free location data
- [Streamlit](https://streamlit.io/) for the rapid UI framework
