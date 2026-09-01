from langchain_community.document_loaders import WebBaseLoader
url = "https://louwersj.medium.com/understanding-langchain-deprecation-warnings-what-they-mean-and-how-to-respond-f9f165c48676"
loader = WebBaseLoader(url)

docs = loader.load()
# print("----------")
# print(len(docs))
# print("----------")
# print(docs[0].page_content)

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

prompt=PromptTemplate(
    template="Answer the question {question} from the following text\n {text}",
    input_variables=['text','question']
    )
parser=StrOutputParser()

chain = prompt | model | parser
result = chain.invoke({'text':docs[0].page_content,'question':"What is this page's info about?"})
print(result)