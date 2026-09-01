from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser=StrOutputParser()

template=PromptTemplate(
    template='Generate 5 interesting facts about the {topic} in one line each ',
    input_variables=['topic']
)


chain = template | model | parser
result = chain.invoke({'topic':"Upside down"})
print(result)

#visualisation of chain
chain.get_graph().print_ascii()
