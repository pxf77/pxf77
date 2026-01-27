from langchain_classic.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.config import get_store
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

store.put(
    ("users",),
    "user_123",
    {
        "name": "苍老师",
        "language": "日语",
    }
)

def get_user_info(config: RunnableConfig) -> str:
    """查找用户信息的函数，可以查看长期记忆中储存的用户信息"""
    # Same as that provided to `create_react_agent`
    store = get_store()
    user_id = config["configurable"].get("user_id")
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

agent = create_react_agent(
    model=model,
    tools=[get_user_info],
    store=store
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "帮我查找长期记忆中储存的用户信息"}]},
    config={"configurable": {"user_id": "user_123"}}
)

print(response['messages'])