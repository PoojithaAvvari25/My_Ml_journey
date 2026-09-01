from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,Optional,Literal

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#schema
#simple typeddict
# class Review(TypedDict):
#     summary: str
#     sentiment: str

#annotated dict

class Review(TypedDict):
    key_themes=Annotated[str,"A list of key themes discussed in the review"]
    summary: Annotated[str ,"A brief summary of the review"]
    sentiment: Annotated[Literal["positive", "negative", "neutral"],"Return sentiment as positive, negative or neutral"]
    pros :Annotated[Optional[list],"Write down all pros in a list"]
    cons:Annotated[Optional[list],"Write down all cons in a list"]
    name:Annotated[Optional[str],"write the name of the  reviewer not product beibg reviewed"]


structured_model=model.with_structured_output(Review)

result=structured_model.invoke("The Samsung Galaxy S26 Ultra delivers high-end performance with a 6.9-inch privacy display and 60W wired charging, though it lacks Qi2 magnetic wireless charging and experiences reduced screen brightness when the privacy feature is active. The device also faces,,,challenges with software bugs, including image artifacts in high-resolution modes and delayed AI feature rollouts. While it remains a productivity powerhouse, these,,deficiencies prevent it from achieving perfection.")

print(result)
print(type(result))
print(result['name'])#optional..will not be there if not mentioned in the review