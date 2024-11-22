import os
import time
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants for space-related keywords
SPACE_KEYWORDS = ["space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", "universe", "rocket", "satellite"]

# Custom CSS for chatbot bubbles and layout
CUSTOM_CSS = """
<style>
/* Chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

/* User message bubble */
.user-message {
    align-self: flex-start;
    background-color: #d1f0ff;
    color: #000000;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 70%;
    font-family: 'Arial', sans-serif;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}

/* Bot message bubble */
.bot-message {
    align-self: flex-end;
    background-color: #1e1e2d;
    color: #ffffff;
    padding: 10px 15px;
    border-radius: 15px;
    max-width: 70%;
    font-family: 'Arial', sans-serif;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}

/* Typing indicator */
.typing-indicator {
    align-self: flex-end;
    background-color: #1e1e2d;
    color: #ffffff;
    padding: 5px 10px;
    border-radius: 15px;
    font-family: 'Arial', sans-serif;
    font-style: italic;
    opacity: 0.7;
}
</style>
"""

# Add CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title
st.title("🪐 Space Chatbot")
st.write("Ask me anything about space and the universe! 🚀")

# Helper function to check if a prompt is space-related
def is_space_related(prompt):
    return any(keyword in prompt.lower() for keyword in SPACE_KEYWORDS)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to simulate bot response typing
def generate_response(user_input):
    if is_space_related(user_input):
        # Simulate thinking process
        time.sleep(1)  # Simulate processing delay
        return f"That's a fascinating question about {user_input}! Here's some information you might find useful."
    else:
        return "Sorry, I can only answer questions about space and the universe. 🌌"

# Chat input box
user_input = st.text_input("Type your message:", key="user_input", placeholder="Ask me about space...")

# Process user input
if user_input:
    # Add user's message to chat history
    st.session_state.chat_history.append({"user": user_input, "bot": None})

    # Generate a bot response
    response = generate_response(user_input)
    st.session_state.chat_history[-1]["bot"] = response

    # Clear input field
    st.session_state.user_input = ""

# Display chat history with bubbles
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    # User message bubble
    st.markdown(f'<div class="user-message">{message["user"]}</div>', unsafe_allow_html=True)

    # Bot message bubble (with typing indicator)
    if message["bot"] is None:
        st.markdown('<div class="typing-indicator">Bot is typing...</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["bot"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
