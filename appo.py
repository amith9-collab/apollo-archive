import streamlit as st
from groq import Groq
from tavily import TavilyClient
import PyPDF2
import base64
import time
import requests # Needed to download the generated image
from io import BytesIO # Needed to handle image data

# ==========================================
# 1. CORE AI ENGINES & API KEYS
# ==========================================
# Use secrets management for security before deploying!
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ==========================================
# 2. EXECUTIVE UI & CSS
# ==========================================
# ==========================================
# 2. EXECUTIVE UI & CSS (MOBILE RESPONSIVE)
# ==========================================
st.set_page_config(page_title="Apollo OS", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    /* 1. Global Base Styles */
    .stApp { background-color: #020617 !important; }
    h1, h2, h3, p, span, div, label { 
        color: #f8fafc !important; 
        font-family: 'JetBrains Mono', monospace !important; 
    }

    /* 2. Standard Desktop Fixes */
    [data-testid="stFileUploader"] section > label { display: none !important; }
    button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 6px !important;
    }

    /* 3. MOBILE-SPECIFIC FIXES (The "Phone View") */
    @media (max-width: 768px) {
        /* Fix the jumbled upload text */
        [data-testid="stFileUploader"] {
            overflow: hidden !important;
        }
        
        /* Reduce font sizes so they don't overlap */
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        
        /* Make the sidebar text smaller so it fits */
        [data-testid="stSidebar"] {
            width: 250px !important;
        }
        
        /* Hide the 'drag and drop' text on mobile since you can't drag on a phone */
        [data-testid="stFileUploaderDropzone"] div div span {
            display: none !important;
        }
        
        /* Force the 'Browse' button to be full width and centered */
        [data-testid="stFileUploaderDropzone"] button {
            width: 100% !important;
            margin: 0 auto !important;
        }
    }

    /* 4. Chat Styling */
    .stChatMessage { 
        background-color: #0f172a !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 10px !important;
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

# --- IMAGE GENERATION FUNCTION ---
def generate_apollo_image(prompt):
    """
    Apollo Imaging Engine (v3.0). 
    Uses a high-speed stable diffusion bridge for real-time visualization.
    """
    try:
        # Since Groq handles Text/Vision, we use a specialized Imaging Bridge
        # For the demo, this creates a high-quality visualization URL
        # Format: https://pollinations.ai/p/[prompt] (Best for stable live demos)
        
        encoded_prompt = prompt.replace(" ", "%20")
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        
        # We ping it to make sure it's ready
        response = requests.get(image_url)
        if response.status_code == 200:
            return image_url
        else:
            return "Generation Error: Imaging Bridge Offline"
    except Exception as e:
        return f"Generation Error: {str(e)}"
        
def encode_image(image_file):
    """Converts camera image to Base64 for Vision analysis."""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def ask_apollo_vision(image_file, user_query):
    """Visual reasoning using Llama 4 Scout (April 2026 standard)."""
    base64_image = encode_image(image_file)
    try:
        response = groq_client.chat.completions.create(
            # Updated to Llama 4 Scout based on previous 404/400 errors
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
    module = st.radio("Access Module:", ["Research Hub", "PDF Intelligence", "Vision Lens", "Imaging Lab", "News Feed"])
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

# --- VISION LENS ---
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

# --- IMAGING LAB (THE NEW CREATIVITY FEATURE) ---
elif module == "Imaging Lab":
    st.title("🎨 Imaging & Visualization Lab")
    
    st.write("Enter a prompt to visualize data or create schematic concepts.")
    image_prompt = st.text_area("Visualization Prompt...", placeholder="A schematic diagram of a solar-powered water filtration system, JetBrains Mono font labels, technical drawing style...")
    
    if st.button("Generate Visualization"):
        if image_prompt:
            with st.spinner("Apollo is synthesizing visual matrices..."):
                image_url = generate_apollo_image(image_prompt)
                
                if "Error" in image_url:
                    st.error(image_url)
                else:
                    st.image(image_url, caption=f"Visualization: {image_prompt[:50]}...")
                    
                    # Add download button for the judges
                    try:
                        image_data = requests.get(image_url).content
                        st.download_button(
                            label="Download Visualization (PNG)",
                            data=image_data,
                            file_name=f"apollo_viz_{int(time.time())}.png",
                            mime="image/png"
                        )
                    except:
                        st.caption("Temporary download link generation failed.")

# --- NEWS FEED ---
elif module == "News Feed":
    st.title("🗞️ Intelligence Feed")
    news = tavily_client.search(query="Latest science and tech news April 2026", search_depth="advanced")
    for r in news['results'][:3]:
        st.write(f"**{r['title']}**")
        st.caption(r['content'])
        st.divider()
