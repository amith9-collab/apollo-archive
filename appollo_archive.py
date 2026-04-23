import streamlit as st
from tavily import TavilyClient

# 1. Page Configuration
st.set_page_config(page_title="Apollo Research Archive", layout="centered")

# 2. PROFESSIONAL UI: Midnight Executive Theme
st.markdown("""
    <style>
    /* Dark, professional background */
    .stApp {
        background-color: #0f172a !important;
    }
    
    /* Clean, Borderless Chat Containers */
    .stChatMessage { 
        background-color: #1e293b !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
        margin-bottom: 15px !important;
    }

    /* Force all text to White/Slate for clarity */
    h1, h2, h3, p, span, div, label { 
        color: #f1f5f9 !important; 
        font-family: 'Inter', -apple-system, sans-serif !important;
    }

    /* Link styling */
    a {
        color: #38bdf8 !important;
        text-decoration: none !important;
        font-weight: 600;
    }

    /* Input Box styling */
    .stChatInput input {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
    
    /* Remove the default user/bot icons completely */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Setup Tavily with your Key
TAVILY_API_KEY = "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"
tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.title("🏛️ Apollo Research Archive")
st.write("Real-time information retrieval system. Enter your inquiry below.")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    # avatar=None and the CSS above ensures NO icons show up
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Professional Search Logic
if prompt := st.chat_input("Inquire the archive..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving global records..."):
            try:
                # Using the whole question for deep context
                response = tavily.search(
                    query=prompt, 
                    search_depth="advanced", 
                    max_results=4
                )
                
                if response['results']:
                    answer = ""
                    for res in response['results']:
                        answer += f"### {res['title']}\n"
                        answer += f"{res['content']}\n"
                        answer += f"**Source:** [Verify Record]({res['url']})\n\n---\n"
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.write("No verified records were found for this inquiry.")
            except Exception as e:
                st.error("Archive Access Denied: Check internet connection.")