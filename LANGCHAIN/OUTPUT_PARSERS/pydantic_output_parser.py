from langchain_core.output_parsers import PydanticOutputParser
from pydantic import Field,BaseModel
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model=ChatGoogleGenerativeAI(model='gemini-2.5-flash')

#pydantic object
class Person(BaseModel):

    name:str = Field(description='Name of the person'),
    age:int = Field(description='Age of the person',gt=18),
    city:str = Field(description='City of the person')

parser=PydanticOutputParser(pydantic_object=Person)

template=PromptTemplate(
    template='Generate the name ,age and city of a fictional {place} character \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

prompt= template.invoke({'place':'india'})

result=model.invoke(prompt)

final_result=parser.parse(result.content)
print(final_result)

print("prompt****")
print(prompt)

# #using chain

# chain = template | model | parser
# result=chain.invoke({'place':"china"})
# print(result)