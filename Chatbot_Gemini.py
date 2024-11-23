# app.py
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import unittest
import joblib
import plotly.express as px

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
        # Use the appropriate model name
        response = genai.generate_text(model="text-bison-001", prompt=prompt)
        return response.result.get('output', "No response generated.")
    except Exception as e:
        return f"Error: {e}"

# Helper function to check if a prompt is space-related
def is_space_related(prompt):
    return any(keyword in prompt.lower() for keyword in SPACE_KEYWORDS)

# Initialize chat history and analytics storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analytics" not in st.session_state:
    st.session_state.analytics = {"questions": [], "responses": []}

# Custom CSS for styling
CUSTOM_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: #1f1f2e;
    color: #fff;
    font-family: Arial, sans-serif;
}
.user-bubble {
    background-color: #d4f1f4;
    color: #000;
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    text-align: left;
}
.bot-bubble {
    background-color: #323edd;
    color: #fff;
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
    text-align: left;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Title
st.title("🪐 Space Chatbot")
st.subheader("Ask me anything about space and the universe! 🚀")

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
    st.session_state.analytics["questions"].append(user_input)
    st.session_state.analytics["responses"].append(len(response.split()))  # Response length for analytics

# Display chat history
for message in st.session_state.chat_history:
    st.markdown(f"<div class='user-bubble'><strong>😊 You:</strong> {message['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'><strong>🤖 Bot:</strong> {message['bot']}</div>", unsafe_allow_html=True)

# Optional analytics using Plotly
if st.session_state.analytics["questions"]:
    st.subheader("Chat Analytics 📊")
    analytics_df = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(pd.DataFrame)(
            {
                "Question": st.session_state.analytics["questions"],
                "Response Length": st.session_state.analytics["responses"]
            }
        )
    )
    fig = px.bar(analytics_df, x="Question", y="Response Length", title="Response Length per Question")
    st.plotly_chart(fig)

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
