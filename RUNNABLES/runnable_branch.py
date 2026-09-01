from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableBranch,RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

prompt1=PromptTemplate(
    template="write a detailed report about {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Summarize the following text \n {text}",
    input_variables=['text']
)

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

parser=StrOutputParser()

report_gen_chain = RunnableSequence( prompt1, model, parser)#prompt1 | model | parser

branch_chain = RunnableBranch(
    (lambda x: len(x.split())>100 ,RunnableSequence(prompt2,model,parser)),
    #else:
    RunnablePassthrough()
    #default
)

final_chain = RunnableSequence(report_gen_chain,branch_chain)
result = final_chain.invoke({'topic':"Canada"})
print(result)