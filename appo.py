import streamlit as st
from groq import Groq
from tavily import TavilyClient
import PyPDF2
import base64
import time
import requests
from io import BytesIO

# ==========================================
# 1. CORE AI ENGINES & API KEYS
# ==========================================
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. MOBILE-FIRST UI & CSS
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    /* Global Base Styles */
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* THE GLITCH KILLER: Force hide overlapping file uploader text */
    [data-testid="stFileUploader"] section > div:nth-child(2),
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }

    /* Style the Sidebar and Navigation */
    [data-testid="stSidebar"] { min-width: 250px !important; }
    
    /* Responsive Buttons */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        height: 3rem !important;
        width: 100% !important;
    }

    /* News Feed Scrollable Box */
    .news-container {
        height: 350px;
        overflow-y: auto;
        padding: 10px;
        background: #0f172a;
        border-radius: 10px;
        border: 1px solid #1e293b;
        font-size: 0.85rem;
    }

    /* Chat Styling */
    .stChatMessage { 
        background-color: #0f172a !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. CORE LOGIC
# ==========================================

def get_apollo_response(user_input, context=""):
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are APOLLO OS. Concise and Professional."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"}
            ],
            model="llama-3.1-8b-instant",
        )
        return completion.choices[0].message.content
    except: return "Neural link error."

def generate_apollo_image(prompt):
    try:
        encoded = prompt.replace(" ", "%20")
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
    except: return "Imaging error."

def ask_apollo_vision(image_file, user_query):
    b64 = base64.b64encode(image_file.getvalue()).decode('utf-8')
    try:
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[{"role": "user", "content": [
                {"type": "text", "text": user_query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]}]
        )
        return response.choices[0].message.content
    except: return "Vision link error."

# ==========================================
# 4. NAVIGATION & SIDEBAR
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    module = st.radio("Access Module:", ["Research Hub", "PDF Intelligence", "Vision Lens", "Imaging Lab", "News Feed"])
    
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. MODULES
# ==========================================

if module == "Research Hub":
    st.title("🏛️ Research Hub")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if p := st.chat_input("Enter inquiry..."):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        res = tavily_client.search(query=p)
        ctx = "\n".join([r['content'] for r in res['results']])
        ans = get_apollo_response(p, ctx)
        with st.chat_message("assistant"): st.write(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})

elif module == "PDF Intelligence":
    st.title("🧠 PDF Intelligence")
    # FIX: label_visibility="collapsed" kills the phone overlap glitch
    up = st.file_uploader("PDF", type="pdf", label_visibility="collapsed")
    if up:
        reader = PyPDF2.PdfReader(up)
        text = "".join([p.extract_text() for p in reader.pages])
        st.success("PDF Analyzed.")
        q = st.text_input("Ask Apollo:")
        if q: st.info(get_apollo_response(q, text[:6000]))

elif module == "Vision Lens":
    st.title("📸 Optical Lens")
    # FIX: camera_input is much more stable for phone presentations
    cam = st.camera_input("Capture Intelligence")
    if cam:
        vq = st.text_input("Analyze for...")
        if vq: st.write(ask_apollo_vision(cam, vq))

elif module == "Imaging Lab":
    st.title("🎨 Imaging Lab")
    ip = st.text_area("Prompt...")
    if st.button("Generate"):
        url = generate_apollo_image(ip)
        st.image(url)

elif module == "News Feed":
    st.title("🗞️ Intelligence Feed")
    with st.spinner("Fetching global news..."):
        news = tavily_client.search(query="Top science and tech headlines April 2026", search_depth="basic")
        # Scrollable container so news doesn't break the layout
        st.markdown('<div class="news-container">', unsafe_allow_html=True)
        for r in news['results'][:6]:
            st.markdown(f"**{r['title']}**")
            st.caption(r['content'][:150] + "...")
            st.divider()
        st.markdown('</div>', unsafe_allow_html=True)
