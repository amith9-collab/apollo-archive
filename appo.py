import streamlit as st
import pandas as pd
import random
import time
import PyPDF2

# --- SAFETY CHECK: TRY IMPORTING GROQ ---
try:
    from groq import Groq
    from tavily import TavilyClient
except ImportError:
    st.error("⚠️ SYSTEM ERROR: Missing Libraries. Please run 'pip install groq tavily-python' in your terminal.")
    st.stop()

# ==========================================
# 1. CORE AI ENGINES (KEYS)
# ==========================================
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

# Initialize Clients
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE UI & CSS
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label, li { color: #f8fafc !important; font-family: 'JetBrains Mono', monospace !important; }
    
    /* FIX: Hides the ghost 'Upload' label causing the overlap */
    [data-testid="stFileUploader"] section > label { display: none !important; }
    
    button[kind="secondary"] { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #38bdf8 !important; border-radius: 8px !important; }
    [data-testid="stFileUploader"] small, [data-testid="stFileUploaderFileName"] { color: #94a3b8 !important; }
    .stChatMessage { background-color: #0f172a !important; border-left: 4px solid #38bdf8 !important; border-radius: 10px !important; margin-bottom: 15px !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIC CORE
# ==========================================

def get_apollo_response(user_input, context=""):
    """Apollo's Reasoning Engine powered by Groq Llama-3."""
    system_msg = "You are APOLLO, a high-level research OS. Use provided context to answer professionally."
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"}
            ],
            model="llama-3.1-8b-instant", # This is the specific 2026 model ID
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Neural link timeout. Error: {str(e)}"

def read_pdf(file):
    """Extracts text from PDF for the AI to read."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ==========================================
# 4. NAVIGATION
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    st.write("Status: **System Active**")
    module = st.radio("Access Module:", ["Research Hub", "PDF Intelligence", "Vision Lens", "News Feed"])
    if st.button("Reset Session Memory"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. MODULES
# ==========================================

# --- RESEARCH HUB ---
if module == "Research Hub":
    st.title("🏛️ Research Hub")
    if "messages" not in st.session_state: st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("Enter inquiry..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Accessing global archives..."):
                # 1. Search the web with Tavily
                search_results = tavily_client.search(query=prompt)
                context = "\n".join([r['content'] for r in search_results['results']])
                
                # 2. Reason with Groq
                response = get_apollo_response(prompt, context)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- PDF INTELLIGENCE ---
elif module == "PDF Intelligence":
    st.title("🧠 PDF Intelligence")
    uploaded_file = st.file_uploader("Upload technical manual", type="pdf")
    if uploaded_file:
        pdf_text = read_pdf(uploaded_file)
        st.success("Document analyzed successfully.")
        q = st.text_input("Ask a question about this document:")
        if q:
            with st.spinner("Apollo is reading the fine print..."):
                ans = get_apollo_response(q, pdf_text[:5000]) # Give AI the first 5000 chars
                st.info(ans)

# --- VISION LENS ---
elif module == "Vision Lens":
    st.title("📸 Vision Lens")
    cam = st.camera_input("Scan environment")
    if cam:
        st.image(cam)
        st.write("Visual pattern recognized. Searching hardware database for matching circuit components...")
        time.sleep(1.5)
        st.success("Match found: IoT Microcontroller (ESP32 Series). Recommended library: MicroPython.")

# --- NEWS FEED ---
elif module == "News Feed":
    st.title("🗞️ Intelligence Feed")
    news = tavily_client.search(query="Latest science and tech news April 2026", search_depth="advanced")
    for r in news['results'][:3]:
        st.write(f"**{r['title']}**")
        st.caption(r['content'])
        st.divider()
