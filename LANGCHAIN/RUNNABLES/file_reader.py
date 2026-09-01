from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
#load the document
loader=TextLoader("docs.txt")
documents=loader.load()

#split text into smaller chunks

text_splitter= RecursiveCharacterTextSplitter(chunk_size=50,chunk_overlap=5)
docs=text_splitter.split_documents(documents)
print(docs)
#convert text into embeddings
vectorstore= FAISS.from_documents(docs,GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"))

#create retriever

retriever=vectorstore.as_retriever()

#manually retrieve relevant docs
query="tell me about japan"
retrieved_docs =retriever.get_relevant_documents(query)

