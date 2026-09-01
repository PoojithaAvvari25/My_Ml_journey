from langchain_huggingface import HuggingFaceEmbeddings

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

document=["Delhi is the capital of india.",
          "The capital of USA is Washington DC.",
          "The capital of France is Paris."]

vectors=embedding.embed_documents(document)
for i, vector in enumerate(vectors):
    print(f"Document {i+1}: {str(vector)}")