from langchain_classic.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

checkpointer = InMemorySaver() # 设置检查点

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

agent = create_react_agent(model=model,
                           tools=[],
                           checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": "1"
    }
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，我叫苍老师，好久不见！"}]},
    config
)

print(response['messages'][-1].content)


response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，请问你还记得我叫什么名字么？"}]},
    config
)

print('------------线程1------------------')
print(response['messages'][-1].content)

new_config = {
    "configurable": {
        "thread_id": "2"
    }
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，请问你还记得我叫什么名字么？"}]},
    new_config
)

print('------------线程2------------------')
print(response['messages'][-1].content)