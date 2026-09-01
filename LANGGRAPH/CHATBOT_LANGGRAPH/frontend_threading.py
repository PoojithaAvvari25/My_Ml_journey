#resuming chat

import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
from uuid import uuid4#generates random thread id every time


#*************8utility functions***************888
def generate_thread_id():
    thread_id = uuid4()
    return thread_id


def reset_chat():
    thread_id = uuid4()
    st.session_state['thread_id']=thread_id
    st.session_state['message_history']=[]
    st.session_state['chat_threads'].append(st.session_state['thread_id'])
    
def add_thread(thread_id):
     if thread_id not in st.session_state['chat_threads']:
          st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    state_values = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values
    # Extract the message list safely from the state dictionary
    # print(state_values.get('messages', []))
    return state_values.get('messages', [])
    
# #to fetch chat history from thread_id
# def load_convo(thread_id):
#      return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values


#******************Session setup*******************


if 'thread_id' not in st.session_state:
     st.session_state['thread_id']=generate_thread_id()


if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'chat_threads' not in st.session_state:
     st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])#this adds thread when we refresh page/start a new session

#**********side bar UI*************

st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'):
     reset_chat()


st.sidebar.header('My conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
     
    if st.sidebar.button(str(thread_id)):#if button is click..have to load chat convo
        messages = load_convo(thread_id)
        st.session_state['thread_id']=thread_id

        temp_messages=[]
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
                temp_messages.append({'role':role,'content':msg})
            else:
                role='assistant'
                temp_messages.append({'role':role,'content':msg})
            
        st.session_state['message_history']=temp_messages
        
             
                

#******************MAIN UI*******************

#loading convo history

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    #add msg to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})

    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):
    
            ai_message = st.write_stream(
                message_chunk.content for message_chunk, metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config = CONFIG,
                    stream_mode ='messages'
                )
            )
    
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    