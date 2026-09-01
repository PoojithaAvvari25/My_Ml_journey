from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import  HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

#llm always understand which message is sent by whom by using this way i.e;by using messages
model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chat_history = [
    SystemMessage(content="You are a helpful assistant.Answer all the queries within 3 lines")
]

while True:
    user_input=input("You:")
    chat_history.append(HumanMessage(content=user_input))
    if user_input.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    result=model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("AI:", result.content)
print(chat_history)