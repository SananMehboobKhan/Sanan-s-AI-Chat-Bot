# ============================================
# app.py - AI Chatbot (Modern UI - Fixed)
# ============================================

import streamlit as st
import time
from datetime import datetime
from search import search_internet
from summarizer import generate_answer
import config

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Sanan AI - Smart Search Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# MODERN CSS - Premium Dark UI (Fixed Input)
# ============================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #111118;
        --bg-card: #16161f;
        --bg-input: #1c1c28;
        --accent: #6c63ff;
        --accent-2: #ff6584;
        --accent-glow: rgba(108, 99, 255, 0.3);
        --text-primary: #f0f0ff;
        --text-secondary: #8888aa;
        --text-muted: #555570;
        --border: rgba(108, 99, 255, 0.2);
        --border-hover: rgba(108, 99, 255, 0.5);
        --success: #00d4aa;
        --radius: 16px;
        --radius-sm: 10px;
    }

    * { font-family: 'Space Grotesk', sans-serif !important; }

    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image:
            linear-gradient(rgba(108,99,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(108,99,255,0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ---- SIDEBAR ---- */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
    }

    /* ---- HEADER ---- */
    .nexus-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 28px 20px 20px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 20px;
    }
    .nexus-logo {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 0 20px var(--accent-glow);
    }
    .nexus-brand {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff, var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .nexus-version {
        font-size: 0.65rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono' !important;
        margin-top: -4px;
    }

    /* ---- STAT CARDS ---- */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 14px 16px;
        margin: 6px 0;
        transition: all 0.2s ease;
    }
    .stat-card:hover {
        border-color: var(--border-hover);
        box-shadow: 0 0 15px var(--accent-glow);
    }
    .stat-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--accent);
        font-family: 'JetBrains Mono' !important;
    }

    /* ---- MAIN TITLE ---- */
    .main-header {
        text-align: center;
        padding: 15px 20px 5px;
        position: relative;
        z-index: 1;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, var(--accent) 50%, var(--accent-2) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .main-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* ---- WELCOME ---- */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px 20px 30px;
        gap: 16px;
    }
    .welcome-icon {
        font-size: 3.5rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
    }
    .welcome-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--text-primary);
        text-align: center;
    }
    .welcome-subtitle {
        color: var(--text-secondary);
        text-align: center;
        font-size: 1rem;
    }
    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        width: 100%;
        max-width: 600px;
        margin-top: 10px;
    }
    .suggestion-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 14px 16px;
        transition: all 0.25s ease;
    }
    .suggestion-card:hover {
        border-color: var(--accent);
        background: var(--bg-input);
        box-shadow: 0 0 20px var(--accent-glow);
        transform: translateY(-2px);
    }
    .suggestion-icon { font-size: 1.2rem; margin-bottom: 6px; }
    .suggestion-text {
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }

    /* ---- CHAT BUBBLES ---- */
    .message-wrapper {
        padding: 6px 0;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-bubble {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
        gap: 10px;
        margin: 12px 0;
    }
    .user-content {
        background: linear-gradient(135deg, var(--accent), #8b7fff);
        color: white;
        padding: 14px 18px;
        border-radius: 20px 20px 6px 20px;
        max-width: 70%;
        font-size: 0.95rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px var(--accent-glow);
    }
    .user-avatar {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 4px;
    }

    .ai-bubble {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 10px;
        margin: 12px 0;
    }
    .ai-avatar {
        width: 36px; height: 36px;
        background: linear-gradient(135deg, #1e1e2e, var(--bg-card));
        border: 2px solid var(--accent);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        margin-top: 4px;
        box-shadow: 0 0 10px var(--accent-glow);
    }
    .ai-content {
        background: var(--bg-card);
        border: 1px solid var(--border);
        color: var(--text-primary);
        padding: 16px 20px;
        border-radius: 6px 20px 20px 20px;
        max-width: 75%;
        font-size: 0.95rem;
        line-height: 1.7;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .ai-content a {
        color: var(--accent) !important;
        text-decoration: none;
    }
    .ai-content a:hover { text-decoration: underline; }

    .msg-time {
        font-size: 0.65rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono' !important;
        margin-top: 4px;
        padding: 0 4px;
    }

    /* ---- INPUT BOX FIX (Most Important!) ---- */
    /* Target every possible streamlit input wrapper */
    .stTextInput { background: transparent !important; }
    .stTextInput > div { background: var(--bg-input) !important; border-radius: 12px !important; border: 1.5px solid var(--border) !important; }
    .stTextInput > div:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; }
    .stTextInput > div > div { background: transparent !important; }
    .stTextInput input,
    .stTextInput > div > div > input,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        background-color: var(--bg-input) !important;
        background: var(--bg-input) !important;
        color: var(--text-primary) !important;
        caret-color: var(--accent) !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        padding: 14px 16px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {
        background-color: var(--bg-input) !important;
        background: var(--bg-input) !important;
        border: none !important;
        border-radius: 12px !important;
    }
    /* Placeholder color */
    .stTextInput input::placeholder,
    div[data-baseweb="base-input"] input::placeholder {
        color: var(--text-muted) !important;
        opacity: 1 !important;
        -webkit-text-fill-color: var(--text-muted) !important;
    }
    /* Autofill fix */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px var(--bg-input) inset !important;
        -webkit-text-fill-color: var(--text-primary) !important;
    }

    /* ---- BUTTONS ---- */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent), #8b7fff) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px var(--accent-glow) !important;
        font-family: 'Space Grotesk' !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px var(--accent-glow) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    .stDownloadButton > button {
        background: transparent !important;
        border: 1px solid var(--border) !important;
        color: var(--text-secondary) !important;
        box-shadow: none !important;
        font-size: 0.85rem !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    /* ---- DIVIDER ---- */
    hr { border-color: var(--border) !important; opacity: 0.4; }

    /* ---- STATUS BADGE ---- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0,212,170,0.1);
        border: 1px solid rgba(0,212,170,0.3);
        color: var(--success);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .status-dot {
        width: 6px; height: 6px;
        background: var(--success);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-size: 0.88rem;
        margin: 2px 0;
    }

    /* ---- SCROLLBAR ---- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

if "search_count" not in st.session_state:
    st.session_state.search_count = 0

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.markdown("""
    <div class="nexus-header">
        <div class="nexus-logo">⚡</div>
        <div>
            <div class="nexus-brand">Sanan AI</div>
            <div class="nexus-version">v1.0.0 · Search Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 0 10px 16px;">
        <span class="status-badge">
            <span class="status-dot"></span>
            ONLINE · Ready to search
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#555570; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; padding: 0 4px;'>Session Stats</p>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Messages</div>
            <div class="stat-value">{st.session_state.message_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Searches</div>
            <div class="stat-value">{st.session_state.search_count}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<p style='color:#555570; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; padding: 0 4px;'>Actions</p>", unsafe_allow_html=True)

    if st.button("🗑️  Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.session_state.search_count = 0
        st.rerun()

    if st.session_state.chat_history:
        history_export = ""
        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "NexusAI"
            history_export += f"[{msg['time']}] {role}:\n{msg['content']}\n\n{'─'*40}\n\n"

        st.download_button(
            label="💾  Export Chat History",
            data=history_export,
            file_name=f"nexusai_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<p style='color:#555570; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; padding: 0 4px;'>How It Works</p>", unsafe_allow_html=True)

    for icon, text in [
        ("🔤", "Type your question"),
        ("🔍", "AI searches DuckDuckGo"),
        ("🧠", "Groq AI summarizes results"),
        ("💬", "Answer appears in chat"),
    ]:
        st.markdown(f"""
        <div class="nav-item">
            <span>{icon}</span>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <br>
    <div style="padding:10px; text-align:center; color:#333355; font-size:0.7rem; border-top:1px solid rgba(108,99,255,0.1);">
        Powered by Groq + DuckDuckGo<br>
        <span style="color:#6c63ff;">Sanan AI</span> · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN AREA
# ============================================

st.markdown("""
<div class="main-header">
    <div class="main-title">⚡ Sanan AI</div>
    <div class="main-subtitle">Ask anything ·</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================
# CHAT DISPLAY
# ============================================

with st.container():

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">🤖</div>
            <div>
                <div class="welcome-title">Hello! I'm Sanan AI</div>
                <div class="welcome-subtitle">I search the internet in real-time and give you smart, summarized answers.</div>
            </div>
            <div class="suggestion-grid">
                <div class="suggestion-card">
                    <div class="suggestion-icon">🌍</div>
                    <div class="suggestion-text">What are the latest world news headlines?</div>
                </div>
                <div class="suggestion-card">
                    <div class="suggestion-icon">🤖</div>
                    <div class="suggestion-text">What is artificial intelligence and how does it work?</div>
                </div>
                <div class="suggestion-card">
                    <div class="suggestion-icon">🐍</div>
                    <div class="suggestion-text">What are the best Python libraries for data science?</div>
                </div>
                <div class="suggestion-card">
                    <div class="suggestion-icon">🚀</div>
                    <div class="suggestion-text">What are the latest developments in space exploration?</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message-wrapper">
                <div class="user-bubble">
                    <div>
                        <div class="user-content">{msg['content']}</div>
                        <div class="msg-time" style="text-align:right;">{msg['time']}</div>
                    </div>
                    <div class="user-avatar">👤</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-wrapper">
                <div class="ai-bubble">
                    <div class="ai-avatar">⚡</div>
                    <div>
                        <div class="ai-content">{msg['content']}</div>
                        <div class="msg-time">{msg['time']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# INPUT AREA
# ============================================

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="✦  Ask me anything...",
        label_visibility="collapsed",
        key="chat_input"
    )

with col2:
    send_btn = st.button("Send  ➤", use_container_width=True, type="primary")

# ============================================
# PROCESS QUESTION
# ============================================

if send_btn and user_input.strip():

    current_time = datetime.now().strftime("%I:%M %p")

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input.strip(),
        "time": current_time
    })
    st.session_state.message_count += 1

    with st.spinner("🔍  working on it..."):
        search_results = search_internet(user_input.strip(), config.MAX_SEARCH_RESULTS)
        st.session_state.search_count += 1

    with st.spinner("🧠  Analyzing and summarizing..."):
        answer = generate_answer(user_input.strip(), search_results)

        if search_results:
            answer += "<br><br><strong>📚 Sources:</strong><br>"
            for i, r in enumerate(search_results[:3], 1):
                answer += f'<a href="{r["url"]}" target="_blank">{i}. {r["title"]}</a><br>'

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer,
        "time": datetime.now().strftime("%I:%M %p")
    })
    st.session_state.message_count += 1

    st.rerun()

elif send_btn:
    st.warning("Please type a question before sending.")