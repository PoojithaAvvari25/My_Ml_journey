from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm=OpenAI(model="gpt-4o-mini")

result=llm.invoke("What is capital of india?")

print(result)

# import os
# from langchain_groq import ChatGroq

# # It is best practice to use environment variables for keys
# # Or just paste it directly for a quick test:


# llm = ChatGroq(model="llama-3.3-70b-versatile")

# result = llm.invoke("What are the capitals of India and France?")
# print(result.content)