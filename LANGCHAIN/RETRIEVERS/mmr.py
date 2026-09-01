from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

docs = [
    Document(page_content="Solar panels convert sunlight directly into clean electrical energy."),
    Document(page_content="Wind turbines harness atmospheric air currents to generate power"),
    Document(page_content="Deep Sea ExplorationThe Mariana Trench is the deepest known point on Earth."),
    Document(page_content="Deep-sea creatures use bioluminescence to glow in complete darkness."),
    Document(page_content="Ancient HistoryThe Great Pyramid of Giza was built for Pharaoh Khufu."),
    Document(page_content="Cuneiform is one of the earliest known forms of writing.")
]

embedding_model=HuggingFaceEmbeddings()

vectorstore=FAISS.from_documents(
    documents=docs,
    embedding=embedding_model
)

#enable mmr in retriever

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs = {"k":3,"lambda_mult":0.5}#lambda_mult=1-->performs normal similarity search,0->gives completely diverse results
)

query="What is deep sea?"
results = retriever.invoke(query)


for i,doc in enumerate(results):
    print(f"\n---Result {i+1}---")
    print(f"Content:\n{doc.page_content}...")