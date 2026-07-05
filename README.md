
# ⚡ LLM Application Using APIs: Dynamic AI Assistant

A production-ready, professional AI Chat Application powered by **Mistral AI** and integrated with **Tavily Search API**. This project demonstrates advanced prompt engineering techniques, state management, and real-time context injection without relying on complex, heavy orchestration agent frameworks (e.g., LangChain Agents). It showcases an optimized workflow built natively on top of API integrations for predictable and fast dynamic response generation.

---

### 🌐 Live Deployment
 https://huggingface.co/spaces/yogesh626813/LLM-API-MODEL  

---

## 🚀 Key Features

- **Dynamic Context Injection (Custom RAG Workflow):** Bypasses heavy multi-agent loops to query the Tavily Search API directly and inject real-time internet context seamlessly into the LLM's system instructions.
- **Optimized Memory State Management:** Utilizes a custom, lightweight rolling history buffer (`st.session_state`) passing exact conversation contexts up to the last 6 interactions, mitigating token bloat while retaining high conversational coherence.
- **Enterprise UI Layout:** Implements an asymmetric, messaging-app style chat interface built using standard Streamlit structures enhanced with professional dark-theme inline CSS.
- **Granular Control Sidebar:** Includes real-time web search toggling and hyperparameter adjustment sliders (e.g., Temperature tuning) for direct user interaction control.
- **Crash Prevention Controls:** Built-in safeguards against empty historical loops and dynamic clearing edge-cases (e.g., IndexError prevention on history reset).

---

## 🛠️ Tech Stack & Architecture

- **Core LLM Platform:** Mistral AI (`mistral-small-2603`) via LangChain Community wrapper.
- **Real-Time Data Engine:** Tavily Search Client API.
- **Frontend / Application Framework:** Streamlit (Python Web Framework).
- **Environment Management:** Python-Dotenv (`.env` containerization).


```

[User Input]
│
▼
[UI Workflow Router]
│
├─► (If Search Enabled) ──► Query Tavily API ──► Fetch Context ──┐
│                                                               │
└───────────────────────────────────────────────────────────────┼──► [Inject Into System Prompt]
│
[Extract Conversation History (Last 6 turns)] ───────────────────────┘
│
▼
[Mistral AI Model] ──► [Structured UI Response Render]

```

---

## ⚙️ Setup & Installation Instructions

Follow these instructions to set up and run the application locally:

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
# On Windows:
    venv\Scripts\activate
# On macOS/Linux:
    source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install streamlit langchain-mistralai tavily-python python-dotenv

```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory of your project and add your API credentials:

```env
MISTRAL_API_KEY=your_actual_mistral_api_key_here
TAVILY_API_KEY=your_actual_tavily_api_key_here

Replace your own api key in env file. Beacause the API kEY is secret so not show here.
```

### 5. Run the Application

```bash
streamlit run UI.py

```

---

## 💡 Prompt Engineering & Integration Insights

Instead of delegating control to an automated agent which can lead to unpredictable loops and high latency, this application demonstrates explicit **Context Augmentation**. When Web Search is toggled:

1. The app extracts key user intents.
2. Formulates a synchronous programmatic request to Tavily.
3. Wraps the results into XML-styled tags (`<Search_Results>...</Search_Results>`) inside the system layout block.
4. Feeds it as a rigid deterministic prompt constraint directly into the Mistral-Small model API.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

---
