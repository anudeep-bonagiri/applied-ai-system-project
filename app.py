import streamlit as st
import os
from src.agent import MusicDJAgent
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI DJ Agent", page_icon="🎵", layout="centered")

st.title("🎵 DJ Byte's Studio")
st.markdown("Chat with the AI DJ! Watch how it uses **Agentic Tools** to fetch recommendations and artist trivia.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = MusicDJAgent()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ GEMINI_API_KEY is not set. Please enter it below to start.")
    user_api_key = st.text_input("Gemini API Key", type="password")
    if user_api_key:
        st.session_state.agent.set_api_key(user_api_key)
        st.success("API Key set successfully!")
        st.rerun()
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "tool_calls" in message and message["tool_calls"]:
                with st.expander("🛠️ Agentic Steps Taken", expanded=False):
                    for call in message["tool_calls"]:
                        st.code(f"> {call}")
            st.markdown(message["content"])

    if prompt := st.chat_input("What kind of music are you in the mood for?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("DJ Byte is hitting the decks..."):
                response_text, tool_calls = st.session_state.agent.send_message(prompt)
                
                if tool_calls:
                    with st.expander("🛠️ Agentic Steps Taken", expanded=True):
                        for call in tool_calls:
                            st.code(f"> {call}")
                            
                st.markdown(response_text)
                
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text,
            "tool_calls": tool_calls
        })

with st.sidebar:
    st.header("Stretch Features Enabled")
    st.markdown("""
    ✅ **RAG Enhancement:** Uses `artist_info.csv`
    ✅ **Agentic Workflow:** Multi-step tool calls
    ✅ **Specialization:** Gen-Z DJ persona via few-shot
    ✅ **Test Harness:** Run `scripts/evaluate_system.py`
    """)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.agent = MusicDJAgent()
        st.rerun()
