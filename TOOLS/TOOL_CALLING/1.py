from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests

load_dotenv()
#create tool

@tool
def multiply(a:int,b:int)->int:
    """Given 2 numbers a and b this tool returns their product"""
    return a*b

print(multiply.invoke({"a":2,"b":3}))

llm=ChatGoogleGenerativeAI(model="gemini-3.6-flash")
#tool binding
llm_with_tools = llm.bind_tools([multiply])
result = llm_with_tools.invoke("can you multiply 3 with 10")#tool call
# print(result)
# print(result.tool_calls)#contains info about tool calls made by llm

args=result.tool_calls[0]['args']

mult_result=multiply.invoke(args)
# print(mult_result)#just result

tool_result2=multiply.invoke(result.tool_calls[0])
print(tool_result2)#wrapped down neatly in ToolMessage--seeing this llm generates its reply

query=HumanMessage("can you multiply 3 with 10")
messages=[query]
llm_reply=llm.invoke(messages)
messages.append(llm_reply)#contains human msg and aii msg(reply of llm)
messages.append(tool_result2)
# print(messages)
#maintaining convo history

res=llm.invoke(messages)
print(res.content)



# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# from langchain_core.tools import tool
# from langchain_core.messages import HumanMessage, ToolMessage # Import ToolMessage
# import requests

# load_dotenv()

# # 1. Create tool
# @tool
# def multiply(a: int, b: int) -> int:
#     """Given 2 numbers a and b this tool returns their product"""
#     return a * b

# llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")
# llm_with_tools = llm.bind_tools([multiply])

# # 2. Start conversation history
# query = HumanMessage("can you multiply 3 with 10")
# messages = [query]

# # 3. First invocation -> Returns AIMessage with tool_calls
# llm_reply = llm_with_tools.invoke(messages) 
# messages.append(llm_reply)

# # 4. Extract tool call info and execute tool
# tool_call = llm_reply.tool_calls[0]
# mult_result = multiply.invoke(tool_call['args'])

# # 5. Explicitly build a ToolMessage to close the model turn loop
# tool_msg = ToolMessage(
#     content=str(mult_result), 
#     name=tool_call['name'], 
#     tool_call_id=tool_call['id']
# )
# messages.append(tool_msg)

# # 6. Final invocation -> Base LLM synthesizes the text response
# res = llm.invoke(messages)
# print(res.content) 
