from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()

prompt=PromptTemplate(
    template="write a joke about {topic}",
    input_variables=['topic']
)

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

parser=StrOutputParser()

chain = RunnableSequence(prompt, model, parser)

result= chain.invoke({"topic":"AI"})

print(result)