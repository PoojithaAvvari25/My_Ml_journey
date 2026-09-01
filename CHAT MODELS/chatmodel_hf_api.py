#not working
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-1B-Instruct",task="text-generation")

model=ChatHuggingFace(llm=llm)

result=model.invoke("What is capital of USA?")
print(result.content)

'''
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the base LLM endpoint
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    temperature=0.5,
    max_new_tokens=100
)

# 2. Wrap it with ChatHuggingFace
model = ChatHuggingFace(llm=llm)

# 3. FIX: ChatHuggingFace expects structured chat messages, not a raw string
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

# 4. Chain the prompt structure to the model
chain = prompt | model

# 5. Execute the chain
result = chain.invoke({"question": "What is the capital of the USA?"})
print(result.content)

'''


