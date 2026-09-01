from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser=JsonOutputParser()

template=PromptTemplate(
    template='Give me the name ,age and city of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}#tells the llm which type of o/p we want--fetched from parser type-here--jsonoutput parser---is filled befor runtime
)
'''
prompt=template.format()

# print(prompt)#prompt will become as--->Give me the name ,age and city of a fictional person Return a JSON object.

result=model.invoke(prompt)

print(result)

final_result=parser.parse(result.content)

print(final_result)
print(type(final_result))#<class 'dict'>--->json output parser returns a dict

'''


#using chains--simpler

chain=template | model | parser 

result=chain.invoke({})

print(result)