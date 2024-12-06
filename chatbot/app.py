import os
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import httpx

with httpx.Client() as client:
    try:
        response = client.get("http://httpbin.org/get", timeout=0.001)
    except httpx.TimeoutException as e:
        print('gottem')
        
llm = OllamaLLM(model="llama3.2:1b")

st.set_page_config(
    page_title="Ollama3.2:1b - Chat",
    page_icon="🗪",
    layout = "centered"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 Ollama3.2:1b - ChatBot")    

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask Ollama3.2:1b...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})


    messages= [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = llm.invoke(messages)
    assistant_response = response
    st.session_state.chat_history.append({"role": "assistant", "content":assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
