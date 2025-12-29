import os
import streamlit as st
from google import genai
from google.genai import types

# API Key (for learning/testing only)
os.environ["GENAI_API_KEY"] = "AIzaSyDP2lnJFFstv8ZbWkHNjKJ1VHtFhmDXkok"

api_key = os.environ.get("GENAI_API_KEY")
if not api_key:
    st.error("API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)
model = "gemini-3-flash-preview"

st.title("Insurance Claims Explainer Bot")
st.write("Ask any question about insurance claim process, documents, or timelines.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Your Question:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    ]

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents
        )

        bot_reply = response.text   # ✅ FIXED LINE

    except Exception as e:
        bot_reply = f"Error generating response: {e}"

    st.session_state.messages.append({"role": "bot", "content": bot_reply})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
