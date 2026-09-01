from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from  pydantic import Field,BaseModel
from typing import Literal
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableLambda #with help of this we can execute multiple chains parallelly
load_dotenv()
# RunnableLambda--can convert a lambda fn into runnable which can be used as a chain

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model2=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser1= StrOutputParser()

class Feedback(BaseModel):
    sentiment:Literal['positive','negative']=Field(description='Give the sentiment of feedback')

parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1=PromptTemplate(
    template='Classify the sentiment of feedback text into positive or negative \n {feedback} \n {format_instruction} ',
    input_variables=['feedback'],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)

classifier_chain= prompt1 | model |parser2 #using pydantic parser always gives us consistent structured result-->here positive/negative only
# result=classifier_chain.invoke({"feedback":"This is a terrible smart phone"})#gives o/p as negative but we have no control on llms o/p ..sometimes it may give other respones other than exactly positive and negative---and the further process of braching only invoves on this output--so we have to use specific structure for that-->usepydantic output parser
result=classifier_chain.invoke({"feedback":"This is a wonderful smart phone"})
# print(result)


prompt2 =PromptTemplate(
    template='Write an appropriate response for this positive feedback in one line \n {feedback}',
    input_variables=['feedback']
)
prompt3 =PromptTemplate(
    template='Write an appropriate response for this negative feedback in one line\n {feedback}',
    input_variables=['feedback']
)
branch_chain = RunnableBranch( #will execute like if elif else type
    # (condition1,chain1),
    # (condition2,chain2),
    # default chain
    (lambda x:x.sentiment=='positive', prompt2 | model | parser1),
    (lambda x:x.sentiment=='negative', prompt3 | model | parser1),
    # default chain
    # lambda x: "could not find sentiment" # this is not chain so we have to convert this lambda function into runnable using some procedure
    RunnableLambda(lambda x: "could not find sentiment")

)

chain = classifier_chain | branch_chain
# result = chain.invoke({'feedback':'This is a terrible smart phone'})
result = chain.invoke({'feedback':'This is a wonderful smart phone'})

print(result)

chain.get_graph().print_ascii()