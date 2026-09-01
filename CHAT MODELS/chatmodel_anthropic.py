from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model=ChatAnthropic(model="claude-3-5-sonnet-20241022")

result=model.invoke("What is capital of USA?")

print(result)

#for open ai chatmodels
'''
from langchain_anthropic import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model="gpt-4",temperature=0.5,max_tokens=10)

result=model.invoke("What is capital of USA?")

print(result.content)
'''