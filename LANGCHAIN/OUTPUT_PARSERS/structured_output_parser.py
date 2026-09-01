from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_classic.output_parsers.structured import ResponseSchema, StructuredOutputParser

#langchain_core--contains important and reusable components
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

schema=[
    ResponseSchema(name="fact_1",description="Fact1 about the topic"),
    ResponseSchema(name="fact_2",description="Fact2 about the topic"),
    ResponseSchema(name="fact_3",description="Fact3 about the topic"),
]

parser=StructuredOutputParser.from_response_schemas(schema)

template=PromptTemplate(
    template='Give 3 facts about the {topic} \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction':parser.get_format_instructions()}#tells the llm which type of o/p we want--fetched from parser type-here--jsonoutput parser---is filled befor runtime
)

prompt=template.invoke({'topic':'black hole'})
#can write template.format also
#using chain
chain = template | model | parser
result=chain.invoke({'topic':'black hole'})
print(result)
'''


result=model.invoke(prompt)
final_result=parser.parse(result.content)
print(final_result)
'''