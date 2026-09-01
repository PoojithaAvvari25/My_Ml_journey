from langchain_huggingface import HuggingFaceEmbeddings

em=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector =em.embed_query("Hello world")
print(vector)