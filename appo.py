import streamlit as st
from groq import Groq
from tavily import TavilyClient
import PyPDF2
import base64
import time
import requests

# ==========================================
# 1. CORE AI ENGINES
# ==========================================
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. THE "NO-GLITCH" CSS
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide")

st.markdown("""
    <style>
    /* Force Dark Mode */
    .stApp { background-color: #020617 !important; }
    * { font-family: 'JetBrains Mono', monospace !important; color: #f8fafc !important; }

    /* THE FIX: Completely hide the broken 'Upload' labels */
    [data-testid="stFileUploader"] section > label, 
    [data-testid="stFileUploader"] section > div:nth-child(2) {
        display: none !important;
    }

    /* Style the Browse button to be clean and simple */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
        color: #38bdf8 !important;
        width: 100% !important;
    }

    /* Fix Sidebar width for mobile */
    [data-testid="stSidebar"] { min-width: 200px !important; }

    /* Clean Chat */
    .stChatMessage { background-color: #0f172a !important; border-radius: 10px; border-left: 3px solid #38bdf8; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIC HUB
# ==========================================

def get_apollo_response(user_input, context=""):
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are APOLLO OS. Answer precisely."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"}
            ],
            model="llama-3.1-8b-instant",
        )
        return completion.choices[0].message.content
    except: return "Neural link error."

def ask_apollo_vision(image_file, user_query):
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    try:
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[{"role": "user", "content": [
                {"type": "text", "text": user_query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}]
        )
        return response.choices[0].message.content
    except: return "Vision link error."

# ==========================================
# 4. MODULES
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    module = st.radio("Access Module:", ["Research Hub", "PDF Intelligence", "Vision Lens", "Imaging Lab"])

if module == "Research Hub":
    st.title("🏛️ Research Hub")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    if prompt := st.chat_input("Query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        search_results = tavily_client.search(query=prompt)
        context = "\n".join([r['content'] for r in search_results['results']])
        res = get_apollo_response(prompt, context)
        with st.chat_message("assistant"): st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

elif module == "PDF Intelligence":
    st.title("🧠 PDF Analysis")
    # Cleaned up uploader
    f = st.file_uploader("Select PDF", type="pdf", label_visibility="collapsed")
    if f:
        reader = PyPDF2.PdfReader(f)
        text = "".join([p.extract_text() for p in reader.pages])
        q = st.text_input("Analyze document:")
        if q: st.info(get_apollo_response(q, text[:5000]))

elif module == "Vision Lens":
    st.title("📸 Optical Lens")
    # On mobile, this will open the phone's native camera
    img = st.camera_input("Scan")
    if img:
        q = st.text_input("Ask about image:")
        if q: st.success(ask_apollo_vision(img, q))

elif module == "Imaging Lab":
    st.title("🎨 Imaging Lab")
    p = st.text_input("Prompt:")
    if st.button("Generate"):
        url = f"https://image.pollinations.ai/prompt/{p.replace(' ', '%20')}?nologo=true"
        st.image(url)
