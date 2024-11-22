 import streamlit as st  
 import google.generativeai as genai  
 genai.configure(api_key="enter your key obtain from aistudio.google.com")  
 model=genai.GenerativeModel(model_name="gemini-pro")  
 st.title("Gemini chat app")  
 if "messages" not in st.session_state:  
   st.session_state.messages=[  
     {  
       "role":"assistant",  
       "content":"enter the question"  
     }  
   ]  
 for message in st.session_state.messages:  
   with st.chat_message( message["role"]) :   
       st.markdown(message["content"])  
 def llmCall(query):  
    response=model.generate_content(query)  
    with st.chat_message("assistant"):  
      st.markdown(response.text)  
    st.session_state.messages.append(  
     {  
       "role": "user",  
       "content": query  
     }  
   )  
    st.session_state.messages.append(  
     {  
       "role": "assistant",  
       "content": response.text  
     }  
   )  
 query=st.chat_input("what is your question?")  
 if query:  
    with st.chat_message("user"):  
      st.markdown(query)    
    llmCall(query=query)  
