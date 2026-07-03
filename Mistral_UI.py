import streamlit as st
import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tavily import TavilyClient

# Load API keys from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Chat Assistant | LLM App",
    page_icon="⚡",
    layout="wide"
)

# --- Custom Professional CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding-bottom: 20px;
    }
    .user-msg {
        align-self: flex-end;
        background-color: #2e6f40;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 0px 18px;
        max-width: 70%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-size: 15px;
        line-height: 1.5;
    }
    .model-msg {
        align-self: flex-start;
        background-color: #1e2329;
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 0px;
        max-width: 80%;
        border: 1px solid #333;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        font-size: 15px;
        line-height: 1.5;
    }
    .search-badge {
        font-size: 11px;
        color: #888;
        margin-bottom: 5px;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8644/8644313.png", width=60)
    st.title("⚙️ AI App Controls")
    st.markdown("### Project: LLM Application Using APIs")
    st.markdown("*Developed with Large Language Model APIs, dynamic prompt engineering, and real-time search automation workflows.*")
    
    st.divider()
    
    st.markdown("### 🛠️ Capabilities")
    use_search = st.toggle("🌐 Enable Web Search (Tavily)", value=False, help="Fetches real-time data from the web before answering.")
    temperature = st.slider("🌡️ Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- Main App UI ---
st.title("⚡ Dynamic AI Assistant")
st.caption("Ask anything. Toggle 'Web Search' in the sidebar for real-time information.")

@st.cache_resource
def get_model(temp):
    return ChatMistralAI(model="mistral-small-2603", temperature=temp)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI assistant. How can I help you today?", "used_search": False}
    ]

# Render Chat History
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        search_indicator = '<span class="search-badge">🔍 Answered using real-time web context</span>' if msg.get("used_search") else ''
        st.markdown(f'<div class="model-msg">{search_indicator}{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Input ---
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# --- Handle AI Response (FIXED LINE HERE) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    current_input = st.session_state.messages[-1]["content"]
    
    with st.spinner("🤖 Processing your request..."):
        model = get_model(temperature)
        system_prompt = "You are a highly capable and professional AI assistant."
        search_context = ""
        
        if use_search:
            try:
                tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
                search_results = tavily_client.search(query=current_input, max_results=3)
                context_texts = [f"- {result['content']}" for result in search_results.get("results", [])]
                search_context = "\n".join(context_texts)
                system_prompt += f"\n\nUse the following real-time web search results to answer the user's query accurately:\n<Search_Results>\n{search_context}\n</Search_Results>"
            except Exception as e:
                st.error(f"Search failed: {e}")
        
        llm_messages = [SystemMessage(content=system_prompt)]
        for msg in st.session_state.messages[-6:]:
            if msg["role"] == "user":
                llm_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                llm_messages.append(AIMessage(content=msg["content"]))
                
        response = model.invoke(llm_messages)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response.content,
            "used_search": use_search
        })
        st.rerun()