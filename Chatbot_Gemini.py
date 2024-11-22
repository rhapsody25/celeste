import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Constants for space-related keywords
SPACE_KEYWORDS = ["space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", "universe", "rocket", "satellite", "black hole", "asteroid", "meteor", "comet", "exoplanet", "nebula", "supernova", "light year", "spacecraft", "space station", "lunar", "solar system", "Milky Way", "interstellar", "astrobiology", "space exploration", "orbit", "constellation", "event horizon", "dark matter", "quasar"]

# Get API Key from .env file for accessing Google Generative Language API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative Language API with API Key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Custom CSS for background and styling
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
    color: #ffffff;
    font-family: 'Arial', sans-serif;
}}

[data-testid="stSidebar"] {{
    background: rgba(0, 0, 0, 0.7);
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
}}

.chat-box {{
    background: rgba(0, 0, 0, 0.5);
    color: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}}

.title {{
    color: #000000;
    font-size: 2em;
    font-weight: bold;
}}

.subtitle {{
    color: #000000;
    font-size: 1.5em;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>🪐 Space Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask me anything about space and the universe! 🚀</div>", unsafe_allow_html=True)

# Helper function to check if a prompt is space-related
def is_space_related(prompt):
    return any(keyword in prompt.lower() for keyword in SPACE_KEYWORDS)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response using Google's Generative Language API
def get_generative_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.result['text']
    except Exception as e:
        st.error(f"Error with Google Generative Language API: {e}")
        return "Sorry, something went wrong while generating a response. Please try again later."

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

# Display chat history
for message in st.session_state.chat_history:
    st.markdown(f"<div class='chat-box'><strong>You:</strong> {message['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-box'><strong>Bot:</strong> {message['bot']}</div>", unsafe_allow_html=True)
