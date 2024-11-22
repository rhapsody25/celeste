import os
import time
import joblib
import base64
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Placeholder: Use a mock for Gemini API as a substitute during testing/debugging
class MockGeminiChat:
    def __init__(self, context, messages):
        self.context = context
        self.messages = messages

    def send_message(self, message, stream=False):
        # Mock response
        if "space" in message.lower():
            return [{"text": "Space is vast and fascinating!"}]
        else:
            return [{"text": "I can only answer questions about space."}]

# Replace `genai` with a mock class for testing
class MockGeminiAPI:
    @staticmethod
    def configure(api_key):
        pass

    @staticmethod
    def chat(context, messages):
        return MockGeminiChat(context, messages)


# Uncomment this when using the real Gemini API
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Using mock API for testing
genai = MockGeminiAPI()

# Create "data" folder if it doesn't exist
if not os.path.exists('data/'):
    os.mkdir('data/')

# Initialize session state variables
if 'chat_id' not in st.session_state:
    st.session_state.chat_id = str(int(time.time()))
if 'chat_title' not in st.session_state:
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"content": "You are an expert in space-related topics. Please answer questions accordingly."}
    ]
if 'gemini_history' not in st.session_state:
    st.session_state.gemini_history = []

# Sidebar for selecting past chats
with st.sidebar:
    st.write('# Past Chats')
    try:
        past_chats = joblib.load('data/past_chats_list')
    except FileNotFoundError:
        past_chats = {}
    st.session_state.chat_id = st.selectbox(
        label='Pick a past chat',
        options=[st.session_state.chat_id] + list(past_chats.keys()),
        format_func=lambda x: past_chats.get(x, 'New Chat' if x == st.session_state.chat_id else f'ChatSession-{x}'),
    )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# Function to validate space-related queries
def is_space_related(query):
    keywords = ["space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", "universe", "rocket", "satellite", "black hole"]
    return any(keyword in query.lower() for keyword in keywords)

# Initialize the chat session
try:
    st.session_state.chat = genai.chat(
        context="You are an expert in space-related topics. Please answer questions accordingly.",
        messages=st.session_state.messages
    )
except Exception as e:
    st.error(f"Error initializing Gemini AI: {e}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message("assistant" if "AI" in message.get('name', '') else "user"):
        st.markdown(message['content'])

# Handle user input
if prompt := st.chat_input('Ask me about space...'):
    if st.session_state.chat_id not in past_chats:
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    # Add user input to messages in the correct format
    st.session_state.messages.append({"content": prompt})

    if is_space_related(prompt):
        try:
            # Send the message and get the response
            response = st.session_state.chat.send_message(prompt, stream=True)
            with st.chat_message(name='ai', avatar='🤖'):
                message_placeholder = st.empty()
                full_response = ''
                for chunk in response:
                    full_response += chunk["text"]
                    message_placeholder.markdown(full_response + '▌')
                message_placeholder.markdown(full_response)

            # Append the AI response
            st.session_state.messages.append({"content": full_response})
        except Exception as e:
            st.error(f"Error during response: {e}")
    else:
        with st.chat_message(name='ai', avatar='🤖'):
            st.markdown("I can only answer questions related to space! 🚀")

    # Save chat data
    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')

# Unit Tests Embedded in Main Code
if __name__ == "__main__":
    import unittest

    class TestIsSpaceRelated(unittest.TestCase):
        def test_valid_space_queries(self):
            queries = [
                "Tell me about the galaxy.",
                "What is the speed of light in space?",
                "NASA launched a new rocket yesterday.",
                "How many planets are in the solar system?",
                "Can you explain black holes?"
            ]
            for query in queries:
                self.assertTrue(is_space_related(query), f"Query failed: {query}")

        def test_invalid_space_queries(self):
            queries = [
                "Tell me about cooking.",
                "What is the stock price of Tesla?",
                "Can you help me with math homework?",
                "How is the weather today?",
                "What is the capital of France?"
            ]
            for query in queries:
                self.assertFalse(is_space_related(query), f"Query failed: {query}")

        def test_edge_cases(self):
            queries = ["", " ", "space", "SPACE exploration"]
            expected_results = [False, False, True, True]
            for query, expected in zip(queries, expected_results):
                self.assertEqual(is_space_related(query), expected, f"Query failed: {query}")

    # Run tests when script is executed directly
    unittest.main()
