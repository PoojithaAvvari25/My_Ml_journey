from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import sqlite3


load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}


connection=sqlite3.connect(database='chatbot.db',check_same_thread=False)#created if db dont exist

# Checkpointer
checkpointer = SqliteSaver(conn=connection)#will not work directly..we have to create db


graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# #test--this stores each thread diff in db..and extracts all prev msgsalong with response  when we run a thread-meansif we ask qn 2nd time we will get 4 msgs in o/p->1st ques,1st response,2nd ques,2nd response
# config={'configurable':{'thread_id':'thread2'}}

# response=chatbot.invoke(
#     {
#         # 'messages':HumanMessage(content="hii my name is poojitha")
#         'messages':HumanMessage(content="what is  my name ")

#     },
#     config=config
# )
# print(response)


def retrieve_all_prev_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return (list(all_threads))#we extracted the unique threads that reside in our db