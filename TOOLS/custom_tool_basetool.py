from langchain_core.tools import BaseTool
from pydantic import BaseModel,Field
from typing import Type

class MultiplyInput(BaseModel):
    a:int = Field(required=True , description="The first number to multiply")
    b:int = Field( json_schema_extra={"required": True},description="The second number to multiply")

class MultiplyTool(BaseTool):
    name:str = "Multiplication",
    description:str = "Multiples two numbers"

    args_schema :Type[MultiplyInput]=MultiplyInput

    def _run(self, a:int,b:int)->int:
        return a*b

multiply_tool = MultiplyTool()

result = multiply_tool.invoke({"a":4,"b":7})
print(result)
print(multiply_tool.name)#prints name of tool
print(multiply_tool.description)#prints doc string provided in fn
print(multiply_tool.args_schema)#prints names,types of arguments 