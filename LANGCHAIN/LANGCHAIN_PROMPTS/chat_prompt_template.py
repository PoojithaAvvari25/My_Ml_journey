from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage,HumanMessage

##the placeholders will not be filled in this way
 #chat_template=ChatPromptTemplate([SystemMessage(content="You are a helpful {domain} expert."),
#                                   HumanMessage(content="explain and answer within 3 lines,what is {topic} ")
#                                   ])


#this will work
chat_template=ChatPromptTemplate([
    ('system',"You are a helpful {domain} expert."),
    ('human', "explain and answer within 3 lines,what is {topic} ")
])
prompt=chat_template.invoke({'domain':'AI','topic':'Langchain'})

print(prompt)
print(prompt.messages)