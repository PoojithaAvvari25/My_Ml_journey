from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
'''
#chatbot without context
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    result=model.invoke(user_input)
    print("AI:", result.content)
'''
#chatbot with context
chat_history = []
while True:
    user_input = input("You: ")
    chat_history.append(user_input)
    if user_input.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break
    result=model.invoke(chat_history)
    chat_history.append(result.content)
    print("AI:", result.content)
print(chat_history)