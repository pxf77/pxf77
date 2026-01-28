from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def get_weather(loc:str)->str:
    """
    根据地点参数可以返回该地点的天气情况
    """
    return f"{loc} 天气是晴！气温23°"

SYSTEM_PROMPT = "你是一个天气助手，具备调用get_weather天气函数获取指定地点天气的能力"

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=SYSTEM_PROMPT
)

question="北京的天气怎么样?"

# 值流模式
# for step in agent.stream(
# {'messages': question},
#     stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

# 非流模式
# print(agent.invoke(
#     {'messages': question},
# )['messages'][-1].content)

# 消息流模式
for token, metadata in agent.stream(
    {'messages': question},
    stream_mode="messages"
):
    print(f"{token.content}", end="")