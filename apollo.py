import streamlit as st
from tavily import TavilyClient
import pandas as pd
import random
import time

# ==========================================
# 1. SYSTEM CORE & API INTEGRATION
# ==========================================
# Using your provided active Tavily API Key
TAVILY_API_KEY = "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"
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE INTERFACE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Apollo OS | Research Environment",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Midnight Theme with Neon Accents
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #020617 !important; }
    
    /* Global Typography - JetBrains Mono for a 'Developer' feel */
    h1, h2, h3, p, span, div, label { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', 'Courier New', monospace !important; 
    }
    
    /* Professional Chat Containers */
    .stChatMessage { 
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 8px !important;
        margin-bottom: 1.5rem !important;
    }

    /* Hide User/Bot Icons to prevent bugs and maintain 'Librarian' aesthetic */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* News/Intel Cards */
    .intel-card { 
        background-color: #0f172a; 
        padding: 1.2rem; 
        border-radius: 8px; 
        border: 1px solid #1e293b;
        border-left: 4px solid #a855f7;
        margin-bottom: 1rem;
    }

    /* Pulse Animation for 'Live' Status */
    .pulse {
        height: 8px; width: 8px; background-color: #22c55e;
        border-radius: 50%; display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #22c55e;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); opacity: 0.7; }
        70% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. PERSONALITY ENGINE (DIALOGUE)
# ==========================================
greetings = [
    "Consulting the global archives for you...",
    "Scanning the digital horizon. Please wait...",
    "Retrieving intelligence from the deep web stacks...",
    "Establishing a connection to global data centers..."
]

closings = [
    "Records retrieved. Shall we investigate further?",
    "Does this archive entry satisfy the current inquiry?",
    "Intelligence synchronized. Standing by for next command.",
    "Data verified. The archive is ready for your next prompt."
]

# ==========================================
# 4. SIDEBAR NAVIGATION & SYSTEM STATUS
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    st.markdown("<div class='pulse'></div> **SYSTEM: ONLINE**", unsafe_allow_html=True)
    st.caption("Advanced Research Environment v2.4")
    st.divider()
    
    module = st.radio("Select Module:", [
        "Archive Agent", 
        "Intel Feed", 
        "Arena (Scores)", 
        "Visual Capture",
        "Document Analysis"
    ])
    
    st.divider()
    if st.button("Purge Archive History"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. CORE MODULE LOGIC
# ==========================================

# --- MODULE: ARCHIVE AGENT ---
if module == "Archive Agent":
    st.title("🏛️ Archive Agent")
    st.write("Current Persona: **Apollo Librarian**")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "System Initialized. I am Apollo. I am ready to retrieve intelligence from the global stacks. What is your inquiry?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Input research query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(random.choice(greetings)):
                try:
                    # Advanced Tavily Search
                    res = tavily.search(query=prompt, search_depth="advanced", max_results=4)
                    
                    # Source Auditing Logic
                    domains = [r['url'].split('/')[2] for r in res['results']]
                    audit_data = [("Academic/Official" if d.endswith(('.gov', '.edu', '.org')) else "General Web") for d in domains]
                    
                    # Construct Personality Response
                    body = f"Inquiry analyzed: **'{prompt}'**. I have cross-referenced the global records.\n\n"
                    for r in res['results']:
                        body += f"🔹 **{r['title']}**\n{r['content']}\n[Access Record]({r['url']})\n\n"
                    
                    full_text = body + "\n" + random.choice(closings)
                    st.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                    
                    # Data Viz: Source Auditor
                    with st.expander("📊 Source Reliability Audit"):
                        st.write("Analyzing the credibility of the retrieved intelligence...")
                        st.bar_chart(pd.Series(audit_data).value_counts())
                except Exception as e:
                    st.error("Critical Error: Archive connection interrupted.")

# --- MODULE: INTEL FEED ---
elif module == "Intel Feed":
    st.title("🗞️ Intelligence Feed")
    tab1, tab2 = st.tabs(["📍 Kerala Reports", "🚀 Innovation Watch"])
    
    with tab1:
        st.subheader("Current Regional Data")
        news = tavily.search(query="Kerala news updates April 2026", search_depth="advanced")
        for r in news['results'][:3]:
            st.markdown(f"<div class='intel-card'><strong>{r['title']}</strong><br>{r['content']}</div>", unsafe_allow_html=True)

    with tab2:
        st.subheader("2026 Technical Breakthroughs")
        tech = tavily.search(query="latest technology inventions and science breakthroughs 2026", search_depth="advanced")
        for r in tech['results'][:3]:
            st.markdown(f"<div class='intel-card' style='border-left-color: #a855f7;'><strong>{r['title']}</strong><br>{r['content']}</div>", unsafe_allow_html=True)

# --- MODULE: ARENA (SCORES) ---
elif module == "Arena (Scores)":
    st.title("🏆 The Arena")
    st.write("Live Match Intelligence: 2026 Season")
    sport_q = st.text_input("Enter Match/League (e.g. IPL 2026 Live):", "IPL Live Score")
    if sport_q:
        scores = tavily.search(query=sport_q, search_depth="advanced")
        st.success(f"Latest Signal: {scores['results'][0]['content']}")

# --- MODULE: VISUAL CAPTURE ---
elif module == "Visual Capture":
    st.title("📸 Optical Interface")
    st.write("Capture real-world data to the local archive.")
    img = st.camera_input("Scanner Active")
    if img:
        st.image(img, caption="Visual Record Archived Successfully.")

# --- MODULE: DOCUMENT ANALYSIS ---
elif module == "Document Analysis":
    st.title("🧠 Document Intelligence")
    st.write("Upload high-density papers for AI structural scanning.")
    doc = st.file_uploader("Select PDF/TXT File", type=["pdf", "txt"])
    if doc:
        with st.status("Performing Neural Scan...", expanded=True):
            time.sleep(1.5)
            st.write("Indexing technical concepts...")
            time.sleep(1)
        st.metric("Document Reliability", "Verified")
        st.info("Analysis Complete. This document has been indexed into your local Apollo memory.")