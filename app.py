# app.py
import streamlit as st
import requests
from config import GROQ_API_KEY, GROQ_MODEL

st.title("Research Assistant with Groq AI")

# Display API key status safely
if GROQ_API_KEY:
    st.write(f"Using API key: {GROQ_API_KEY[:4]}***")
else:
    st.error("❗ GROQ_API_KEY is missing! Add it in Streamlit Secrets.")

st.write(f"Default model: {GROQ_MODEL}")

# Input box for user prompt
user_input = st.text_area("Enter your question or prompt:")

if st.button("Generate Response"):
    if not user_input:
        st.warning("Please enter a prompt first!")
    elif not GROQ_API_KEY:
        st.error("Cannot generate response without API key!")
    else:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": GROQ_MODEL, "messages": [{"role": "user", "content": user_input}], "max_tokens": 200}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            st.success(answer)
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling Groq API: {e}")
