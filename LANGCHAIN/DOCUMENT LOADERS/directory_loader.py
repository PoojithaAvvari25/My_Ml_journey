from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader

loader = DirectoryLoader(
    path = "C:/Users/pooji/Desktop/Infosys_offer",
    glob = "*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load() #swaps each doc in and out of memory

for doc in docs:
    print(doc.metadata)



# print(docs[0].page_content)
# print(docs[0].metadata)
# print(len(docs))