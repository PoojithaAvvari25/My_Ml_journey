from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel
from dotenv import load_dotenv

load_dotenv()

prompt1 = PromptTemplate(
    template="generate 2 names of a {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="generate 2 nick names of a {topic}",
    input_variables=['topic']
)
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

parser=StrOutputParser()

parallel_chain = RunnableParallel(
    {
        'names' : RunnableSequence(prompt1, model ,parser),
        'nick names':RunnableSequence(prompt2,model,parser)
    }
)

result = parallel_chain.invoke({'topic':'girl'})
print(result)
print(result['names'])
print(result['nick names'])