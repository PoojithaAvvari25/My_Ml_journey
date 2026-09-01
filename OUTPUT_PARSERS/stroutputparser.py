# from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# load_dotenv()

# llm=HuggingFaceEndpoint(
#     repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
#     #cant able to give str o/p by defuault
#     task="text-generation"
# )

# model=ChatHuggingFace(llm=llm)

# #1 prompt---> detailed report
# template1=PromptTemplate(
#     template="'Write a detailed report on {topic}",
#     input_variables=['topic']
# )

# #2 prompt---> short summary

# template2=PromptTemplate(
#     template='write a five line summary of the following text /n {text}',
#     input_variables=['text']

# )

# prompt1=template1.invoke({'topic':'black hole'})

# result=model.invoke(prompt1)

# prompt2=template2.invoke({'text': result.content})

# result1=model.invoke(prompt2)

# print(result1.content)




from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")


#1 prompt---> detailed report
template1=PromptTemplate(
    template="'Write a detailed report on {topic}",
    input_variables=['topic']
)

#2 prompt---> short summary

template2=PromptTemplate(
    template='write a 5 line summary of the following text /n {text}',
    input_variables=['text']

)

prompt1=template1.invoke({'topic':'black hole'})

result=model.invoke(prompt1)

prompt2=template2.invoke({'text': result.content})

result1=model.invoke(prompt2)

print(result1.content)