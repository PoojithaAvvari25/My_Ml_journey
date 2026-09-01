from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents=["Japan is a beautiful island nation in Asia.",
           "The country of Japan has many mountains.",
           "Brazil is the largest country in South America.",
           "Many people speak Portuguese in Brazil.",
           "France attracts millions of international tourists every year."]

# query="what is the largest country in South America?"
# query="what is the island nation in Asia?"
# query="what attracts international tourists every year?"
query="tell me about japan"




query_embedding=embedding.embed_query(query)
doc_embeddings=embedding.embed_documents(documents)

similarity_scores=cosine_similarity([query_embedding], doc_embeddings)

print(similarity_scores)

index,score=sorted(list(enumerate(similarity_scores[0])),key=lambda x: x[1],reverse=True)[0]
print(f"Query: {query}")
print(f"Most similar document: {documents[index]} \n with similarity score: {score}")