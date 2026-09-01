from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
#initialsie llm

llm=ChatGoogleGenerativeAI(model ="gemini-2.5-flash",temperature=0.7)

#create propt template
prompt=PromptTemplate(
    input_variables=["topic"],
    template="Suggest a title for a story book{topic}. "
    )

#define i/p

topic=input('Enter a topic')

formatted_prompt=prompt.format(topic=topic)

story_title=llm.invoke(formatted_prompt)

print("Generated story title: ",story_title)
