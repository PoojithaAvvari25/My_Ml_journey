from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ShellTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor,create_react_agent
from dotenv import load_dotenv
import requests
from langchain.tools import tool
from pydantic import BaseModel, Field


load_dotenv()

@tool
def get_weather_data(coordinates: str) -> str:
    """This function fetches the current weather data from a given coordinates string formatted as 'latitude=X, longitude=Y'"""
    # Quick parsing logic to extract floats from the string line
    parsed = dict(item.split("=") for item in coordinates.replace(" ", "").split(","))
    latitude = float(parsed["latitude"])
    longitude = float(parsed["longitude"])
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=03ef10178cae928d907a8bf20bdec67b'
    response = requests.get(url)
    return response.json()

search_tool = DuckDuckGoSearchRun()
results=search_tool.invoke('top news in india today ')
# print(results)

llm=ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

# prompt = pull("hwchase17/react")
from langchain_core.prompts import PromptTemplate

# This is the exact underlying template text pulled from hwchase17/react
react_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

# Reconstruct the template object for create_react_agent
prompt = PromptTemplate.from_template(react_template)

react_agent=create_react_agent(
        llm=llm,
        tools=[search_tool,get_weather_data],
        prompt=prompt
)

agent_executor = AgentExecutor(
    agent=react_agent,
    tools=[search_tool,get_weather_data],
    verbose=True
)

result=agent_executor.invoke({"input":" find the capital of India and then find its weather conditions"})
print(result)
print(result['output'])#user sees
