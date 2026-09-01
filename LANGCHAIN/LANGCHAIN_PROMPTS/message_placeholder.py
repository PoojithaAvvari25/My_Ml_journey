from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
#chat template

chat_template = ChatPromptTemplate([
    ('system', "You are a helpful  agent."),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human',"{query}")
])


#create prompt

prompt = chat_template.invoke({'chat_history': 
                               [("human", "Hi, what is 2+2?"), 
                                ("ai", "2+2 is 4.")],
                                'query':'multiply it with 4'
                                })

print(prompt)

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
result=model.invoke(prompt)
print(result.content)