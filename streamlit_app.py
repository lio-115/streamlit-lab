import uuid

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Streamlit 실습", page_icon="🤖")

if "cache_id" not in st.session_state:
    st.session_state.cache_id = str(uuid.uuid4())

with st.sidebar:
    st.title("설정")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        key="api_key",
    )

if api_key:
    st.session_state.openai_client = OpenAI(api_key=api_key)
else:
    st.session_state.pop("openai_client", None)

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Home", icon="🏠"),
    st.Page("app_pages/Chat.py", title="Chat", icon="💬"),
    st.Page("app_pages/Chatbot.py", title="Chatbot", icon="📚"),
    st.Page("app_pages/ChatPDF.py", title="ChatPDF", icon="📄"),
])

pg.run()