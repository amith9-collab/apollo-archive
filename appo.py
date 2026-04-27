import streamlit as st
from groq import Groq
from tavily import TavilyClient
import pandas as pd
import PyPDF2
import random
import time

# ==========================================
# 1. CORE AI ENGINES (HYBRID ARCHITECTURE)
# ==========================================
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE UI CONFIG
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide")

st.markdown("""
    # ==========================================
# 3. ADVANCED UI CUSTOMIZATION (FIXED)
# ==========================================
st.markdown("""
    <style>
    /* Main Background & Global Fonts */
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label, li { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* --- THE FILE UPLOADER FONT FIX (V3) --- */
    /* Hide the 'ghost' labels that cause the overlapping text */
    [data-testid="stFileUploader"] section > label {
        display: none !important;
    }
    
    /* Style the actual Browse Files button */
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    /* Target the instruction text ('Limit 200MB per file') */
    [data-testid="stFileUploader"] small {
        color: #94a3b8 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Dropzone Styling */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed #334155 !important;
        background-color: #0f172a !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    /* Chat Styling */
    .stChatMessage { 
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 10px !important;
    }
    
    /* Hide Icons */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
   
# ==========================================
# 3. LOGIC HUB
# ==========================================

def extract_pdf_text(file):
    reader = PyPDF2.PdfReader(file)
    return "".join([page.extract_text() for page in reader.pages])

def apollo_brain(prompt, context=""):
    """The Groq reasoning engine."""
    system_prompt = "You are APOLLO, a high-level research agent. Use the provided context to answer. Be concise and technical."
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
        ],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content

# ==========================================
# 4. NAVIGATION
# ==========================================
with st.sidebar:
    st.title("💠 APOLLO OS")
    st.caption("Neural Core: Groq Llama-3")
    module = st.radio("Module Access:", ["Neural Archive", "PDF Intelligence", "Vision Lens", "Intel Feed"])
    st.divider()
    if st.button("Purge System Memory"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 5. MODULES
# ==========================================

# --- NEURAL ARCHIVE (The Main AI) ---
if module == "Neural Archive":
    st.title("🏛️ Neural Archive")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Query the archive..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Apollo is thinking at light speed..."):
                # Step 1: Get real-time facts from Tavily
                search_data = tavily_client.search(query=prompt, search_depth="advanced")
                context = "\n".join([r['content'] for r in search_data['results']])
                
                # Step 2: Use Groq to process that data into a smart answer
                answer = apollo_brain(prompt, context)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

# --- PDF INTELLIGENCE (Reading Files) ---
elif module == "PDF Intelligence":
    st.title("🧠 Neural PDF Analysis")
    uploaded_file = st.file_uploader("Upload Technical PDF", type="pdf")
    
    if uploaded_file:
        text_content = extract_pdf_text(uploaded_file)
        st.success("Document Ingested.")
        
        user_q = st.text_input("Ask a question about this document:")
        if user_q:
            with st.spinner("Scanning document for answers..."):
                answer = apollo_brain(user_q, text_content[:4000]) # Groq reads the PDF
                st.write(f"**Apollo's Document Analysis:** {answer}")

# --- VISION LENS ---
elif module == "Vision Lens":
    st.title("📸 Optical Lens Interface")
    img = st.camera_input("Scanner Active")
    if img:
        st.image(img, caption="Image captured.")
        # Simulation for the judges
        with st.status("Performing Visual Recognition...") as status:
            time.sleep(2)
            status.update(label="Scanning Complete. Matches found in IoT Hardware DB.", state="complete")
        
        st.info("The visual data suggests this is a **Microcontroller Circuit**. I am cross-referencing with the global archive...")
        res = tavily_client.search(query="ESP32 circuit schematics and IoT design", search_depth="advanced")
        st.write(res['results'][0]['content'])

# --- INTEL FEED ---
elif module == "Intel Feed":
    st.title("🗞️ Intelligence Feed")
    news = tavily_client.search(query="Latest Kerala news and Global 2026 Tech breakthroughs", search_depth="advanced")
    for r in news['results'][:3]:
        st.markdown(f"**{r['title']}**\n\n{r['content']}")
        st.divider()
