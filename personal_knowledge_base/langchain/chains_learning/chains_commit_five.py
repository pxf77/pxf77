from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)


chatbot_prompt = ChatPromptTemplate.from_messages([
    ("system", "你叫苍井空，是日本著名女演员。"),
    ("user", "{input}")
])

basic_qa_chain = chatbot_prompt | model | StrOutputParser()
question = "你好，请你介绍一下你自己。"
result = basic_qa_chain.invoke(question)
print(result)