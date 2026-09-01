from langchain_core.tools import StructuredTool
from pydantic import Field,BaseModel

class MultiplyInput(BaseModel):
    a:int = Field(required=True , description="The first number to multiply")
    b:int = Field( json_schema_extra={"required": True},description="The second number to multiply")

def multiply_func(a:int,b:int)->int:
    return a*b

mult_tool=StructuredTool.from_function(
    func=multiply_func,
    name="Multiplication",
    args_schema=MultiplyInput,
    description="Multiply two numbers"
)

result = mult_tool.invoke({"a":3,"b":5})
print(result)
print(mult_tool.name)#prints name of tool
print(mult_tool.description)#prints doc string provided in fn
print(mult_tool.args)#prints names,types of arguments 
