from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

#schema
#simple typeddict
# class Review(TypedDict):
#     summary: str
#     sentiment: str

#json schema
json_schema={
    "title":"Review",
    "type":"object",
    "properties":{
        "key_themes":{
            "type":"array",
            "items":{
                "type":"string"
            },
            "description":"A list of key themes discussed in the review"
        },
        "summary":{
            "type":"string",
            "description":"A brief summary of the review"
        },
        "sentiment":{
            "type":"string",
            "enum":["pos","neg","neu"],
            "description":"Return sentiment as positive, negative or neutral"
                    
        },
        "pros":{
            "type":["array","null"],
            "items":{
                "type":"string"
            },
            "description":"Write down all pros in a list"
        },
        "cons":{
            "type":["array","null"],
            "items":{
                "type":"string"
            },
            "description":"Write down all cons in a list"
        },
        "name":{
            "type":["string","null"],
            "description":"write the name of the  reviewer not product beibg reviewed"
        }

        },
        "required":["key_themes","sentiment","summary"]
}


structured_model=model.with_structured_output(json_schema)

result=structured_model.invoke("The Samsung Galaxy S26 Ultra delivers high-end performance with a 6.9-inch privacy display and 60W wired charging, though it lacks Qi2 magnetic wireless charging and experiences reduced screen brightness when the privacy feature is active. The device also faces,,,challenges with software bugs, including image artifacts in high-resolution modes and delayed AI feature rollouts. While it remains a productivity powerhouse, these,,deficiencies prevent it from achieving perfection.")

print(result)
print(type(result))
print(result.name)
print(dict(result))#converting pydantoc object into python dictionary
