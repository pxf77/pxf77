from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


@tool
def get_weather(loc:str)->str:
    """
    根据地点参数可以返回该地点的天气情况
    """
    return f"{loc} 天气是晴！气温23°"

SYSTEM_PROMPT = "你是一个天气助手，具备调用get_weather天气函数获取指定地点天气的能力"

model = init_chat_model(
    model="qwen-plus",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=SYSTEM_PROMPT,
    middleware=[HumanInTheLoopMiddleware(
        interrupt_on={
            "get_weather": {
                "allowed_decisions": ["approve", "reject"]
            }
        }
    )],
    checkpointer=InMemorySaver()
)

config = {
    "configurable": {
        "thread_id": "1"
    }
}

result = agent.invoke(
    {
        "messages": "今天北京天气怎么样?"
    },
    config
)

# 同意场景
# if "__interrupt__" in result:
#     result = agent.invoke(
#         Command(
#             resume={"decisions": [{"type": "approve"}]}
#         ),
#         config
#     )

# 拒绝场景
if "__interrupt__" in result:
    result = agent.invoke(
        Command(
            resume={"decisions": [{"type": "reject", "message": "用户拒绝执行"}]}
        ),
        config
    )

for msg in result['messages']:
    msg.pretty_print()