#contextual compression retriever

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.documents import Document
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(
        page_content="""The Grand Canyon is one of the most visited natural wonders in the world.
Photosynthesis is the process by which green plants convert sunlight into energy.
Millions of tourists travel to see it every year. The rocks date back millions of years.""",
        metadata={"source": "Doc1"}
    ),
    Document(
        page_content="""In medieval Europe, castles were built primarily for defense.
The chlorophyll in plant cells captures sunlight during photosynthesis.
Knights wore armor made of metal. Siege weapons were often used to breach castle walls.""",
        metadata={"source": "Doc2"}
    ),
    Document(
        page_content="""Basketball was invented by Dr. James Naismith in the late 19th century.
It was originally played with a soccer ball and peach baskets. NBA is now a global league.""",
        metadata={"source": "Doc3"}
    ),
    Document(
        page_content="""The history of cinema began in the late 1800s. Silent films were the earliest form.
Thomas Edison was among the pioneers. Photosynthesis does not occur in animal cells.
Modern filmmaking involves complex CGI and sound design.""",
        metadata={"source": "Doc4"}
    )
]

embedding_model = HuggingFaceEmbeddings()

#faiss vector store
vs=FAISS.from_documents(
    documents=docs,
    embedding=embedding_model
)

base_retriever = vs.as_retriever(search_kwargs={"k":5})

#setup compressor using an llm
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
compressor = LLMChainExtractor.from_llm(llm)

#create ccr
ccr=ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

query = "what is photosynthesis?"
compressed_results = ccr.invoke(query)

for i,doc in enumerate(compressed_results):
    print(f"\n---Result {i+1}---")
    print(f"Content:\n{doc.page_content}...")
