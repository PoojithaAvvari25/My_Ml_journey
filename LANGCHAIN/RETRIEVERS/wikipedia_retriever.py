from langchain_community.retrievers import WikipediaRetriever

#initialise retriever
retriever = WikipediaRetriever(top_k_results=2,lang="en")

#define your query
query = "the eiffel tower in paris"

#get relevant wikipedia docs
docs=retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"\n---Result {i+1}---")
    print(f"Content:\n{doc.page_content}...")



# --------will only work in python versions upto 3.12-------