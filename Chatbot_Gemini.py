import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from .env file for accessing Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Gemini API with API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Custom CSS for chatbot layout and chat bubbles
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

# Add CSS to Streamlit app
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title and description
st.title("🪐 Space Chatbot")
st.write("Ask me anything about space and the universe! 🚀")

# Helper function to check if a prompt is space-related
def is_space_related(prompt):
    space_keywords = ["space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", "universe", "rocket", "satellite", "black hole", "asteroid", "meteor", "comet", "exoplanet", "nebula", "supernova", "light year", "spacecraft", "space station", "lunar", "solar system", "Milky Way", "interstellar", "astrobiology", "space exploration", "orbit", "constellation", "event horizon", "dark matter", "quasar"]
    return any(keyword in prompt.lower() for keyword in space_keywords)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response using Google's Generative AI API
def get_gemini_response(prompt):
    try:
        response = genai.chat(
            context="You are a knowledgeable assistant specialized in space and the universe. Please answer questions in a simple and clear way.",
            messages=[{"content": prompt}]
        )
        return response["candidates"][0]["content"]
    except Exception as e:
        st.error(f"Error with Gemini API: {e}")
        return "Sorry, something went wrong while generating a response. Please try again later."

# User input
user_input = st.text_input("Type your message:", key="user_input", placeholder="Ask me about space...")

# Process user input
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"user": user_input, "bot": None})

    # Check if the question is space-related
    if is_space_related(user_input):
        # Generate response from Gemini API
        with st.spinner("Bot is typing..."):
            bot_response = get_gemini_response(user_input)
    else:
        bot_response = "Sorry, I can only answer questions about space and the universe. 🌌"

    # Add bot response to chat history
    st.session_state.chat_history[-1]["bot"] = bot_response

    # Clear input field
    st.session_state.user_input = ""

# Display chat history in bubbles
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    # User message bubble
    st.markdown(f'<div class="user-message">{message["user"]}</div>', unsafe_allow_html=True)

    # Bot message bubble
    if message["bot"] is None:
        st.markdown('<div class="typing-indicator">Bot is typing...</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["bot"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
