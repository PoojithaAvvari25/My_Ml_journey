from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.tools import InjectedToolArg
from typing import Annotated
import requests
import json

load_dotenv()

@tool
def get_conversion_factor(base_currency:str,target_currency:str)->float:
    """This functions fetches the currency conversion factor between the given base currency and a target currency"""
    url=f'https://v6.exchangerate-api.com/v6/43ac506dd6be3ea7daf20d8d/pair/{base_currency}/{target_currency}'
    response=requests.get(url)
    return response.json()

# print(get_conversion_factor.invoke({'base_currency':"USD","target_currency":"INR"}))


#url-to get conversion factor-->https://v6.exchangerate-api.com/v6/43ac506dd6be3ea7daf20d8d/pair/USD/INR
@tool
def convert(base_curr_value:int,conversion_factor:Annotated[float,InjectedToolArg])->float:#means dont fill value this urself--i (developer)wioll inject this value after running previous tools
    """ This function calculates the target currency value from a given base currency value and currency conversion rate"""
    return base_curr_value*conversion_factor

#tool binding
llm = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")
llm_with_tools = llm.bind_tools([get_conversion_factor,convert])
# messages = [HumanMessage("What is the conversion factor between USD and INR ? After fetching  that  convert 10 USD into INR")]
messages = [HumanMessage("Perform two tasks simultaneously using your tools: "
        "1. Fetch the conversion factor between USD and INR. "
        "2. Convert exactly 10 USD into INR using the conversion tool. "
        "Provide both tool calls at the same time.")]
ai_message=llm_with_tools.invoke(messages)

# print(ai_message.tool_calls)#gives 2 tools in result-->only base currency value is set..not conversion_factor

for tc in ai_message.tool_calls:
    #execute 1st tool andget the value of conversion rate
    if tc ['name']== "get_conversion_factor":
        tool_message1=get_conversion_factor.invoke(tc)
        # print(tool_message1)
        #fetch this conversion rate
        response_dict = json.loads(tool_message1.content)
        conversion_rate = response_dict['conversion_rate']
        #execute the second tool using the conversion rate from tool1
        messages.append(tool_message1)
    elif tc['name']=="convert":
        tc['args']['conversion_factor'] = conversion_rate
        tool_message2 = convert.invoke(tc)
        # print(tool_message2)
        messages.append(tool_message2)

        # print(messages)
print(messages)
print("************")
print(llm.invoke(messages).content)
