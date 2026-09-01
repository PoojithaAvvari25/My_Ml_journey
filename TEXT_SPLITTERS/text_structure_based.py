from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


text = """The Silent Sun
A quiet spark in river sand,  
A heavy weight within the hand.  
It does not rust, it does not fade,  
By fire and pressure softly made.  

The kings may rise, the kings may fall,  
This yellow sun outlives them all.  
No tarnish mars its sacred light,  
A steady glow against the night.  

Deep in the dark of ancient stone,  
It waited for the light alone.  
Through centuries of ice and rain,  
Unchanged by sorrow, time, or pain.  

Men sail across the stormy sea,  
To trade their lives for alchemy.  
They dig the earth and bleed the vein,  
For fleeting wealth and short-lived gain.  

Yet still it keeps its secret cold,  
The ageless majesty of gold.  
A silent crown, a lasting spark,  
That never leaves us in the dark.
"""

splitter=RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=0
)

chunks = splitter.split_text(text)
print(chunks)