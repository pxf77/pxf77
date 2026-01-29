from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

model = init_chat_model(
    model="qwen-plus",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

agent = create_agent(
    model=model,
    checkpointer=InMemorySaver()
)

result = agent.invoke(
    {
        "messages": "你好我叫石原里美?"
    },
    {
        "configurable": {
            "thread_id": "1"
        }
    }
)

for msg in result['messages']:
    msg.pretty_print()

result = agent.invoke(
    {
        "messages": "你好我叫什么名字?"
    },
{
        "configurable": {
            "thread_id": "1"
        }
    }
)

for msg in result['messages']:
    msg.pretty_print()