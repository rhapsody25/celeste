# Import semua modul yang dibutuhkan
import time  # Untuk mencatat waktu (timestamp)
import os  # Untuk berinteraksi dengan sistem operasi (misalnya, membuat folder)
import joblib  # Untuk menyimpan dan mengambil data
import streamlit as st  # Untuk membuat tampilan web sederhana
import google.generativeai as genai  # Untuk berkomunikasi dengan API Gemini (chatbot)
from dotenv import load_dotenv  # Untuk memuat file .env yang berisi kunci API

# Memuat variabel-variabel dari file .env
load_dotenv()

# Mendapatkan API Key dari file .env, yang akan digunakan untuk mengakses API Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Konfigurasi API Gemini menggunakan API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Membuat ID unik untuk setiap chat baru
new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'  # Peran sebagai AI (chatbot)
AI_AVATAR_ICON = '✨'  # Ikon untuk avatar chatbot

# Membuat folder "data" jika belum ada. Folder ini digunakan untuk menyimpan chat lama.
if not os.path.exists('data/'):
    os.mkdir('data/')

# Memuat daftar chat lama (jika ada). Kita simpan daftar ini di file `data/past_chats_list`
try:
    past_chats = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar untuk memilih chat lama
with st.sidebar:
    st.write('# Past Chats')  # Judul di sidebar
    # Jika belum ada chat yang dipilih, pilih dari daftar chat lama atau buat chat baru
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',  # Label pilihan chat
            options=[new_chat_id] + list(past_chats.keys()),  # Pilihan chat (baru dan lama)
            format_func=lambda x: past_chats.get(x, 'New Chat'),  # Nama chat yang ditampilkan
            placeholder='_',
        )
    else:
        # Memilih chat yang sudah ada jika pengguna pernah memilih chat sebelumnya
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x,
                                                 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    # Set judul chat yang sedang dipilih
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# Menampilkan judul utama aplikasi
st.write('# Chat with Gemini')

# Coba memuat riwayat pesan chat jika ada
try:
    # Pesan dan riwayat dari Gemini disimpan di file, kita coba memuatnya di sini
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    st.session_state.gemini_history = joblib.load(f'data/{st.session_state.chat_id}-gemini_messages')
except:
    # Jika belum ada, mulai dengan pesan kosong
    st.session_state.messages = []
    st.session_state.gemini_history = []

# Membuat model AI generative Gemini
st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

# Menampilkan semua pesan yang ada dalam riwayat chat
for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])  # Menampilkan isi pesan

# Reaksi terhadap input pengguna
if prompt := st.chat_input('Your message here...'):
    # Simpan chat jika ID chat tidak ada dalam daftar chat lama
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')

    # Menampilkan pesan pengguna di chat
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append(dict(role='user', content=prompt))

    # Mengirim pesan pengguna ke API Gemini dan menampilkan balasan dari AI
    response = st.session_state.chat.send_message(prompt, stream=True)
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        message_placeholder = st.empty()  # Tempat untuk menampilkan pesan
        full_response = ''

        # Menampilkan balasan dengan animasi karakter demi karakter
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)  # Menunggu sedikit waktu sebelum menampilkan karakter berikutnya
                message_placeholder.write(full_response + '▌')  # Efek typing
        message_placeholder.write(full_response)

    # Menyimpan pesan balasan AI ke riwayat
    st.session_state.messages.append(dict(role=MODEL_ROLE, content=full_response, avatar=AI_AVATAR_ICON))
    st.session_state.gemini_history = st.session_state.chat.history

    # Menyimpan pesan dan riwayat Gemini ke file
    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')
