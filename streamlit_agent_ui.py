import streamlit as st
import os
import time
import requests
from dotenv import load_dotenv
from openai import OpenAI

# ---------- ENV + API Setup ----------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ Missing OpenAI API key in .env")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Streamlit Page Setup ----------
st.set_page_config(page_title="AutoInsight AI", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚙️ Navigation")
    st.markdown("Choose an option below:")
    mode = st.radio("Mode", ["AI Insights", "Web Search + AI"])
    
    st.markdown("---")
    st.markdown("### 🔑 API Status")
    if OPENAI_API_KEY:
        st.success("✅ OpenAI Connected")
    else:
        st.error("❌ OpenAI Missing")

    if SERPER_API_KEY:
        st.success("✅ Serper Connected")
    else:
        st.warning("⚠️ Serper Missing")

    st.markdown("---")
    st.markdown("💬 *Start your vehicle chat in the main window*")

# ---------- Header ----------
st.markdown("""
<div style="text-align:center; margin-top:15px;">
    <h1 style="color:#60a5fa;">AutoInsight AI</h1>
    <p style="color:#9ca3af;">Your intelligent co-pilot for vehicle analysis, comparisons, trends, and insights</p>
</div>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Helper: Serper Search ----------
def search_serper(query):
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        data = res.json()
        if "organic" in data and len(data["organic"]) > 0:
            results = [f"- [{r['title']}]({r['link']})\n{r['snippet']}" for r in data["organic"][:5]]
            return "\n\n".join(results)
        else:
            return "No relevant results found."
    except Exception as e:
        return f"⚠️ Search failed: {e}"

# ---------- Helper: OpenAI Response ----------
def ai_response(user_input, mode="AI Insights"):
    context = ""

    # If web search mode, add live results
    if mode == "Web Search + AI" and SERPER_API_KEY:
        context = search_serper(user_input)
        context = f"\nHere are live web results:\n{context}\n\nUse these results to give a current and accurate answer.\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant specialized in vehicle data, comparisons, specs, and trends."},
            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            {"role": "user", "content": context + user_input},
        ],
    )
    return response.choices[0].message.content

# ---------- Chat Interface ----------
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role_class = "right" if message["role"] == "user" else "left"
        bg_color = "#2d3748" if message["role"] == "user" else "#1a202c"
        st.markdown(f"""
        <div style='background:{bg_color}; border-radius:8px; padding:10px; margin:6px; text-align:{role_class};'>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# ---------- Input ----------
user_input = st.chat_input("Ask about vehicles, features, comparisons, or trends...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div style='text-align:right; background:#2d3748; padding:10px; border-radius:8px; margin:6px;'>{user_input}</div>", unsafe_allow_html=True)

    ai_reply = ai_response(user_input, mode)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Typing effect
    typing_placeholder = st.empty()
    typing_text = ""
    for ch in ai_reply:
        typing_text += ch
        typing_placeholder.markdown(f"<div style='text-align:left; background:#1a202c; padding:10px; border-radius:8px; margin:6px;'>{typing_text}</div>", unsafe_allow_html=True)
        time.sleep(0.01)
