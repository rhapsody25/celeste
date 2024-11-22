import os
import time
import joblib
import base64
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from .env file for accessing Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Gemini API with API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Create "data" folder if it doesn't exist. This folder is used to store past chats.
if not os.path.exists('data/'):
    os.mkdir('data/')

# Initialize session state variables
if 'chat_id' not in st.session_state:
    st.session_state.chat_id = str(int(time.time()))
if 'chat_title' not in st.session_state:
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an expert in space-related topics. Please answer questions accordingly."}
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

# Add CSS for improved styling
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("images.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://cdn.zmescience.com/wp-content/uploads/2015/06/robot.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    opacity: 0.9;
    color: #ffffff;
    font-family: 'Arial', sans-serif;
}}

[data-testid="stSidebar"] {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    opacity: 0.85;
    color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
}}

[data-testid="stChatInput"] {{
    background: rgba(255, 255, 255, 0.2);
    color: #000000;
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
    border: 2px solid #ffffff;
    font-family: 'Courier New', Courier, monospace;
}}

[data-testid="stMarkdownContainer"] {{
    font-size: 1.2em;
    line-height: 1.5;
    color: #ffffff;
    background: rgba(0, 0, 0, 0.5);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}}

[data-testid="stHeader"], [data-testid="stToolbar"] {{
    background: rgba(0, 0, 0, 0) !important;
    color: #ffffff;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to validate space-related queries
def is_space_related(query):
    keywords = ["space", "astronomy", "planet", "galaxy", "star", "NASA", "cosmos", "universe", "rocket", "satellite"]
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
    with st.chat_message(name=message['role'], avatar=message.get('avatar', '🤖')):
        st.markdown(message['content'])

# Handle user input
if prompt := st.chat_input('Ask me about space...'):
    if st.session_state.chat_id not in past_chats:
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    # Add user input to messages
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if is_space_related(prompt):
        response = st.session_state.chat.send_message(prompt, messages=st.session_state.messages, stream=True)
        with st.chat_message(name='ai', avatar='🤖'):
            message_placeholder = st.empty()
            full_response = ''
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + '▌')
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "ai", "content": full_response, "avatar": '🤖'})
    else:
        with st.chat_message(name='ai', avatar='🤖'):
            st.markdown("I can only answer questions related to space! 🚀")

    # Save chat data
    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')
