from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough,RunnableParallel
from dotenv import load_dotenv

load_dotenv()

# passthrough = RunnablePassthrough()
# print(passthrough.invoke({'2'}))

prompt1 = PromptTemplate(
    template="generate a joke of a {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="generate explanation of the following joke \n {joke}",
    input_variables=['joke']
)
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

parser=StrOutputParser()

joke_gen_chain = RunnableSequence(prompt1, model ,parser)

parallel_chain = RunnableParallel(
    {
        'joke' : RunnablePassthrough(),
        'explanation':RunnableSequence(prompt2,model,parser)
    }
)

final_chain = RunnableSequence(joke_gen_chain,parallel_chain)
result = final_chain.invoke({'topic':'Computer'})
print(result)
