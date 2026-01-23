from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="你叫斋藤飞鸟，是日本著名女演员。"),
    MessagesPlaceholder(variable_name="messages"),
])

chain = prompt | model | parser

messages_list = [] # 初始化历史
print(" 输入 exit 结束对话")
while True:
    user_query = input("你：")
    if user_query.lower() in {"exit", "quit"}:
        break

    # 1）追加用户消息
    messages_list.append(HumanMessage(content=user_query))

    # 2）调用模型
    assistant_reply = ''
    print('斋藤飞鸟:', end=' ')
    for chunk in chain.stream({"messages": messages_list}):
        assistant_reply += chunk
        print(chunk, end="", flush=True)
    print()

    # 3）追加 AI 回复
    messages_list.append(AIMessage(content=assistant_reply))

    # 4）仅保留最近50条
    messages_list = messages_list[-50:]