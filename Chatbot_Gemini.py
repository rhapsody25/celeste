# app.py
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import unittest

# Load environment variables from .env file
load_dotenv()

# Constants for space-related keywords
SPACE_KEYWORDS = [
    "space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", 
    "universe", "rocket", "satellite", "black hole", "asteroid", "meteor", 
    "comet", "exoplanet", "nebula", "supernova", "light year", "spacecraft", 
    "space station", "lunar", "solar system", "Milky Way", "interstellar", 
    "astrobiology", "space exploration", "orbit", "constellation", 
    "event horizon", "dark matter", "quasar"
]

# Get API Key from .env file for accessing Google Generative Language API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative Language API with API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to generate response using Google's Generative Language API
def get_generative_response(prompt):
    try:
        response = genai.generate_text(model="gemini-1.5-flash", prompt=prompt)
        return response.result if 'text' in response.result else "No response generated."
    except Exception as e:
        return f"Error: {e}"

# Custom CSS for bubble chat layout and background
BACKGROUND_IMAGE_URL = "https://cdn.zmescience.com/wp-content/uploads/2015/06/robot.jpg"
CUSTOM_CSS = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{BACKGROUND_IMAGE_URL}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    font-family: 'Arial', sans-serif;
}}

.chat-bubble {{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}}

.user-bubble {{
    background-color: #d4f1f4;
    color: #000;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    margin-left: 10px;
    max-width: 70%;
    word-wrap: break-word;
    display: inline-block;
}}

.bot-bubble {{
    background-color: #323edd;
    color: #fff;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    margin-left: 10px;
    max-width: 70%;
    word-wrap: break-word;
    display: inline-block;
}}

.icon {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: inline-block;
}}

.user-icon {{
    background-image: url("https://i.imgur.com/JY5lT02.png");
    background-size: cover;
    background-position: center;
}}

.bot-icon {{
    background-image: url("https://i.imgur.com/5qH2GjI.png");
    background-size: cover;
    background-position: center;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title
st.markdown("<div style='font-size: 2em; font-weight: bold; color: white;'>🪐 Space Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size: 1.2em; color: white;'>Ask me anything about space and the universe! 🚀</div>", unsafe_allow_html=True)

# Helper function to check if a prompt is space-related
def is_space_related(prompt):
    return any(keyword in prompt.lower() for keyword in SPACE_KEYWORDS)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.text_input("Enter your message:")

# Process the user's input
if user_input:
    if is_space_related(user_input):
        with st.spinner("Bot is typing..."):
            response = get_generative_response(user_input)
    else:
        response = "Sorry, I can only answer questions about space and the universe. 🌌"

    # Update chat history
    st.session_state.chat_history.append({"user": user_input, "bot": response})

# Display chat history with bubble layout
for message in st.session_state.chat_history:
    st.markdown(
        f"""
        <div class="chat-bubble">
            <div class="icon user-icon"></div>
            <div class="user-bubble">😊 {message['user']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="chat-bubble">
            <div class="icon bot-icon"></div>
            <div class="bot-bubble">🤖 {message['bot']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Unit Tests ---
class TestSpaceChatbot(unittest.TestCase):
    def test_is_space_related(self):
        # Positive cases
        self.assertTrue(is_space_related("Tell me about galaxies."))
        self.assertTrue(is_space_related("What is a black hole?"))
        self.assertTrue(is_space_related("NASA missions"))
        # Negative cases
        self.assertFalse(is_space_related("What is the weather today?"))
        self.assertFalse(is_space_related("Who is the president?"))
    
    def test_get_generative_response(self):
        # Test response generation with a mock prompt
        response = get_generative_response("Tell me about the Milky Way galaxy.")
        self.assertIsInstance(response, str)  # Ensure the response is a string
        self.assertNotEqual(response, "")  # Ensure the response is not empty

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
