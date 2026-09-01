import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
# #building chat_message and chat_input components

# with st.chat_message('user'):#can use avatar param also
#     st.text('hi')

# with st.chat_message('assistant'):
#     st.text('hello')

# user_input =st.chat_input('Type here')
# if user_input:
#     with st.chat_message('user'):
#         st.text(user_input)


#st.session_state-> dict ->will not reset until we manually refresh a page,so hitting enter will not effect this
if 'msg_history' not in st.session_state:
    st.session_state['msg_history']=[]
# msg_history=[]#but this wont work..because if we hit enter script runs from forst and this dictionary  resets
#loading chat history

for msg in st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input =st.chat_input('Type here')

if user_input:

    #add msg to history
    st.session_state['msg_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    config={'configurable':{'thread_id':'1'}}
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
    reply= response['messages'][-1].content[0]['text']
    st.session_state['msg_history'].append({'role':'assistant','content':reply})
    with st.chat_message('assistant'):
         st.text(reply)

    