from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableLambda,RunnablePassthrough,RunnableParallel
from dotenv import load_dotenv

load_dotenv()

def word_counter(text):
    return len(text.split())
# word_counter_runnable = RunnableLambda(word_counter)
# print(word_counter_runnable.invoke("hi hello hi"))
prompt=PromptTemplate(
    template="write a joke about {topic}",
    input_variables=['topic']
)

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

parser=StrOutputParser()

joke_gen_chain = RunnableSequence(prompt,model,parser)

# parallel_chain = RunnableParallel({
#     'joke' : RunnablePassthrough(),
#     'word_count': RunnableLambda(word_counter)
# })

parallel_chain = RunnableParallel({
    'joke' : RunnablePassthrough(),
    'word_count': RunnableLambda(lambda x:len(x.split()))
})

final = RunnableSequence(joke_gen_chain,parallel_chain)
result=final.invoke({'topic':'computer'})
# print(result)
final_result = """joke - {} \n word count - {}""".format(result['joke'],result['word_count'])
print(final_result)