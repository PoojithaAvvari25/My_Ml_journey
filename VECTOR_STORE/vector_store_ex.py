from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# 1. FIXED: Imported Document from the correct langchain_core package
from langchain_core.documents import Document

d1 = Document(
     page_content= "Deep learning algorithms are revolutionizing autonomous driving systems. Vehicles utilize neural networks to process real-time video feeds from cameras, allowing them to detect pedestrians, read traffic signs, and navigate complex urban intersections safely.",
     metadata= {"topic": "Artificial Intelligence", "category": "Healthcare & Tech"}
)  
d2 = Document(
     page_content= "The Amazon Rainforest stands as the largest tropical rainforest on Earth, spanning nine South American nations. It acts as a massive carbon sink and shelters roughly 10% of the world's known biodiversity, making its preservation vital for global climate stability.",
    metadata = {"topic": "Ecology", "category": "Environment"} 
)  
d3 = Document(
     page_content= "Silicon-based quantum dots are emerging as a leading platform for scalable quantum computing. Researchers manipulate the spin of individual electrons trapped in these semiconductor nanostructures to create stable qubits with low error rates.",
     metadata =  {"topic": "Quantum Computing", "category": "Advanced Physics"}
)
d5 = Document(
     page_content="French pastry chefs rely on precise temperature control and lamination to create flaky croissants. Layering cold butter between sheets of yeast-leavened dough creates hundreds of microscopic pockets that expand during baking, resulting in a crisp, airy texture.",
     metadata = {"topic": "Culinary Arts", "category": "Baking"}
)
d4 = Document(
     page_content="The Scientific Revolution during the 16th and 17th centuries fundamentally altered human views of the natural world. Thinkers like Galileo Galilei and Isaac Newton established the empirical method, prioritizing mathematical logic and observation over scholastic tradition.",
     metadata =  {"topic": "History", "category": "Science History"}
)

docs = [d1, d2, d3, d4, d5]

embeddings = HuggingFaceEmbeddings()

vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embeddings
)

# Replace the "persisent_directory" keyword by saving to disk manually
vector_store.save_local("faiss_db")

print("Vector store successfully created and saved locally!")
print(vector_store)
# Define your test search query
query = "Tell me about quantum computing advancements"

# Run similarity search (k=2 returns top 2 matches)
results = vector_store.similarity_search_with_score(query, k=2)

print("\n--- Search Results ---")
for doc, score in results:
    # A lower L2 distance score means higher semantic similarity
    print(f"\n[Score (Distance): {score:.4f}]")
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
print("-------------------------------------------------------")
# Query about tech, but strictly filtered for the "Advanced Physics" category
query = "Tell me about computing advancements"

results = vector_store.similarity_search(
    query=query,
    k=1,
    filter={"category": "Advanced Physics"}
)

# Output will only return the Quantum Computing document (d3)
print(results[0].page_content)
print(results[0].metadata)

#some changes will be there if we work with croma
