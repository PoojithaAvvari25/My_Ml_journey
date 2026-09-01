from langchain_core.tools import tool

# step1-create fn-add type hinting and doc string
#step2-add tool decorator
@tool
def multiply(a:int,b:int)->int:
    """multiply two numbers"""
    return a*b

result = multiply.invoke({"a":2,"b":3})
print (result)
print(multiply.name)#prints name of tool
print(multiply.description)#prints doc string provided in fn
print(multiply.args)#prints names,types of arguments 
print(multiply.args_schema.model_json_schema())#this info will be sent to llm about the tool when it is connected to the llm