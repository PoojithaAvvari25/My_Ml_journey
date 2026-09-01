from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader("Offer Letter.pdf")
docs=loader.load()
print(docs)
print(len(docs))