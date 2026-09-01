from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

prompt=PromptTemplate(
    template="Write a summary for the following poem\n {poem}",
    input_variables=['poem']
    )
parser=StrOutputParser()

def f():
    loader = TextLoader('gold_poem.txt',encoding='utf-8')

    docs = loader.load()  #contains list of documents
    return docs[0].page_content

# print(docs)#includes metadata and page content
# print(docs[0].metadata)
# print(type(docs))
runnablee = RunnableLambda(lambda x:f())
chain = runnablee | prompt | model | parser #we can also write w/o using runnable and directly passing docs[0].page_content to the chain as i/p variable
result = chain.invoke({})
print(result)