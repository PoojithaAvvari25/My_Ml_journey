import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})




'''
import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

#st.session_state-> dict ->will not reset until we manually refresh a page,so hitting enter will not effect this
if 'msg_history' not in st.session_state:
    st.session_state['msg_history']=[]

for msg in st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input =st.chat_input('Type here')
# VERY IMPORTANT
if user_input is None:
    st.stop()
    
if user_input:
    #add msg to history
    st.session_state['msg_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)



with st.chat_message("assistant"):
    response=""
    for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": "1"}},
                stream_mode="messages"
    ):
        content=message_chunk.content
        if isinstance(content,list):
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    if text:
                        response += text
                        st.write(response)
    
                # In case content is a normal string
                elif isinstance(content, str):
                    response += content
                    st.write(response)
    
        

    # Save AI response
    st.session_state.msg_history.append({
        "role": "assistant",
        "content": response
    })


    # with st.chat_message('assistant'):
    #     # ai_message=st.write_stream(
    #     #     message_chunk.content 
    #         for message_chunk,metadata in chatbot.stream(
    #             {'messages':[HumanMessage(content=user_input)]},
    #                 config={'configurable':{'thread_id':'1'}},
    #                 stream_mode='messages'
    #         ):
    #              st.write(message_chunk)
    #         # if isinstance(message_chunk.content,str)
    # #     )
    # # st.session_state['msg_history'].append({'role':'assistant','content':ai_message})
    

'''