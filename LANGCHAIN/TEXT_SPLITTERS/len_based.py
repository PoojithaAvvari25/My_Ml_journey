from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


# text = """The Silent Sun

# A quiet spark in river sand,  
# A heavy weight within the hand.  
# It does not rust, it does not fade,  
# By fire and pressure softly made.  

# The kings may rise, the kings may fall,  
# This yellow sun outlives them all.  
# No tarnish mars its sacred light,  
# A steady glow against the night.  

# Deep in the dark of ancient stone,  
# It waited for the light alone.  
# Through centuries of ice and rain,  
# Unchanged by sorrow, time, or pain.  

# Men sail across the stormy sea,  
# To trade their lives for alchemy.  
# They dig the earth and bleed the vein,  
# For fleeting wealth and short-lived gain.  

# Yet still it keeps its secret cold,  
# The ageless majesty of gold.  
# A silent crown, a lasting spark,  
# That never leaves us in the dark.
# """

# splitter=CharacterTextSplitter(
#     chunk_size=80,
#     chunk_overlap=0
# )

# res = splitter.split_text(text)
# print(res)

loader = PyPDFLoader('Offer Letter.pdf')
docs = loader.load()

splitter=CharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0
)

result = splitter.split_documents(docs)
print(len(result))
print(result[2].page_content)

#By default, its separator is a double newline (\n\n). If an entire page of your PDF does not have a double newline, CharacterTextSplitter will keep the text together in one massive chunk, completely ignoring your chunk_size=200 setting. 