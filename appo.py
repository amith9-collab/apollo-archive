import streamlit as st
from groq import Groq
from tavily import TavilyClient
import PyPDF2
import base64
import time

# ==========================================
# 1. CORE AI ENGINES & API KEYS
# ==========================================
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE UI & CSS (STABLE VERSION)
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* Professional Button Styling */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
    }

    /* Uploader Dropzone Fix */
    [data-testid="stFileUploaderDropzone"] {
        border: 1px solid #334155 !important;
        background-color: #0f172a !important;
        border-radius: 10px !important;
    }

    /* Chat Styling */
    .stChatMessage { 
        background-color: #0f172a !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 10px !important;
        margin-bottom: 15px !important;
    }
    
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { 
        display: none !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIC HUB (THE BRAINS)
# ==========================================

def get_apollo_response(user_input, context=""):
    """Text-based reasoning using Llama 3.1 Instant."""
    system_msg = "You are APOLLO, a high-level research OS. Use provided context to answer professionally."
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_input}"}
            ],
            model="llama-3.1-8b-instant",
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Neural link timeout. Error: {str(e)}"

def encode_image(image_file):
    """Converts camera image to Base64 for the AI to 'see'."""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def ask_apollo_vision(image_file, user_query):
    """Visual reasoning using Llama 3.2 Vision."""
    base64_image = encode_image(image_file)
    try:
        response = groq_client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_query},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Optical Analysis Error: {str(e)}"

def read_pdf(file):
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
                search_results = tavily_client.search(query=prompt)
                context = "\n".join([r['content'] for r in search_results['results']])
                response = get_apollo_response(prompt, context)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- PDF INTELLIGENCE ---
elif module == "PDF Intelligence":
    st.title("🧠 PDF Intelligence")
    uploaded_file = st.file_uploader("Upload technical manual", type="pdf")
    if uploaded_file:
        pdf_text = read_pdf(uploaded_file)
        st.success("Document analyzed.")
        q = st.text_input("Ask a question about this document:")
        if q:
            with st.spinner("Apollo is reading..."):
                ans = get_apollo_response(q, pdf_text[:6000])
                st.info(ans)

# --- VISION LENS (THE NEW FEATURE) ---
elif module == "Vision Lens":
    st.title("📸 Optical Intelligence")
    img = st.camera_input("Capture Intelligence")
    if img:
        st.image(img, caption="Visual Record Captured.")
        vision_query = st.text_input("Analyze this image for...")
        if vision_query:
            with st.spinner("Apollo is analyzing visual patterns..."):
                analysis = ask_apollo_vision(img, vision_query)
                st.info(f"**Visual Analysis:** {analysis}")

# --- NEWS FEED ---
elif module == "News Feed":
    st.title("🗞️ Intelligence Feed")
    news = tavily_client.search(query="Latest science and tech news April 2026", search_depth="advanced")
    for r in news['results'][:3]:
        st.write(f"**{r['title']}**")
        st.caption(r['content'])
        st.divider()
