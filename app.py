import streamlit as st
import requests
import json

# Streamlit page setup
st.set_page_config(page_title="AI Language Tutor", layout="centered")
st.title("🎓 Interactive Language Learning AI")

# Styling: red, white, black
st.markdown("""
    <style>
    body { background-color: black; color: white; }
    h1 { color: red; }
    .stTextInput input {
        background-color: white !important;
        color: black !important;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: red;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    .message-container {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .user { background-color: #222; color: white; }
    .ai { background-color: #111; color: red; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Input box
user_input = st.text_input("Ask me anything about language learning:")

# Ask button
if st.button("Ask"):
    if user_input:
        # Add user input to conversation
        st.session_state.conversation.append(f"You: {user_input}")
        
        # Build full prompt history
        conversation_text = "\n".join(st.session_state.conversation)
        prompt = conversation_text + "\nAI:"

        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
            headers = {"Content-Type": "application/json"}

            with st.spinner("Thinking..."):
                response = requests.post(url, json=payload, headers=headers)
                reply = response.json().get("response", "").strip()

            st.session_state.conversation.append(f"AI: {reply}")

        except Exception as e:
            reply = f"An error occurred: {e}"
            st.session_state.conversation.append(f"AI: {reply}")
    else:
        st.warning("Please enter a question!")

# Display conversation
st.markdown("### Conversation")
for message in st.session_state.conversation:
    if message.startswith("You:"):
        st.markdown(f"<div class='message-container user'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-container ai'>{message}</div>", unsafe_allow_html=True)
