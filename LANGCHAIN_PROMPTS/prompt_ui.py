from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.header('Research tool')


user_input=st.text_input("Enter your prompt here:")
#this is static prompt--where user should pass diff prompt each time for diff requirements
if user_input:
    result = model.invoke(user_input)
    

if st.button('Summarize'):
    st.write(result.content)