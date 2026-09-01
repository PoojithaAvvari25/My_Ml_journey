from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate,load_prompt
import streamlit as st

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.header('Reasearch Tool')

paper_input = st.selectbox( "Select Research Paper Name", 
                           ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", 
                           ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", 
                            ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

# 
# '''
# #template

# template = PromptTemplate(
#     input_variables=["paper_input", "style_input", "length_input"],
#     template="Summarize the research paper '{paper_input}' in a {style_input} style with a {length_input} length."
# )
# '''
# 

template=load_prompt('template.json')
#fill the place holders

prompt = template.invoke({
    'paper_input': paper_input,
    'style_input': style_input, 
    'length_input': length_input
})



# #can directly invoke both model and prompt template once withpout using two invoke steps
# chain=template| model
# result=chain.invoke({
#     'paper_input': paper_input,
#     'style_input': style_input, 
#     'length_input': length_input
# })
# if st.button('Summarize'):
#     st.write(result.content)

#     #this also works
# ##  
if st.button('Summarize'):
    result = model.invoke(prompt)
    st.write(result.content)