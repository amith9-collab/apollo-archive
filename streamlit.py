import streamlit as st
from tavily import TavilyClient
import pandas as pd
import random
import time

# ==========================================
# 1. CORE SYSTEM & API
# ==========================================
TAVILY_API_KEY = "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"
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Apollo OS",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 3. ADVANCED UI CUSTOMIZATION (STRICT CSS)
# ==========================================
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label, li { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* --- THE FILE UPLOADER FONT FIX --- */
    /* Target the Browse Files button */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
    }
    
    /* Target the text inside the uploader (Instructions & File Name) */
    [data-testid="stFileUploaderFileName"], 
    [data-testid="stMarkdownContainer"] p,
    .st-emotion-cache-1ae8kda, 
    .st-emotion-cache-zt5igj { 
        color: #94a3b8 !important; 
        font-size: 0.85rem !important;
    }
    
    /* Target the dropzone box */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #334155 !important;
        background-color: #0f172a !important;
        border-radius: 12px !important;
    }

    /* Chat Styling */
    .stChatMessage { 
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 10px !important;
    }
    
    /* Hide Default Icons */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* News Cards */
    .intel-card { 
        background-color: #0f172a; 
        padding: 1.2rem; 
        border-radius: 10px; 
        border-left: 4px solid #a855f7;
        margin-bottom: 1rem;
        border-top: 1px solid #1e293b;
        border-right: 1px solid #1e293b;
        border-bottom: 1px solid #1e293b;
    }

    /* Status Pulse */
    .pulse {
        height: 10px; width: 10px; background-color: #22c55e;
        border-radius: 50%; display: inline-block;
        margin-right: 10px;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.9); opacity: 0.7; }
        70% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. PERSONALITY REPERTOIRE
# ==========================================
greetings = ["Consulting the archives...", "Scanning global data nodes...", "Establishing secure link to research stacks..."]
closings = ["Intelligence verified.", "Standing by for further inquiry.", "Data added to session memory."]

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    st.markdown("<div class='pulse'></div> **CORE: ACTIVE**", unsafe_allow_html=True)
    st.divider()
    module = st.radio("Access Wing:", ["Archive Agent", "Intel Feed", "Document Analysis", "Arena (Scores)", "Visual Input"])
    st.divider()
    if st.button("Purge System Memory"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 6. MODULES
# ==========================================

# --- ARCHIVE AGENT ---
if