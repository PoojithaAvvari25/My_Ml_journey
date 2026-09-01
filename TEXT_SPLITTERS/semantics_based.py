from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
#wont run need openai subscription
# Initialize embedding model and chunker
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = SemanticChunker(
    embeddings,breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=1
    )

# Split your text or documents
docs = text_splitter.create_documents(["Cricket is a popular team sport played with a bat and ball. Two teams take turns trying to score runs.Paris is the capital city of France. It is famous for the Eiffel Tower and great art.India is a very large country in South Asia. It has the second-highest number of people in the world. Its capital city is New Delhi."])
print(docs)
