import requests
from langchain_core.tools import tool
from langchain_classic.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field


class WeatherQuery(BaseModel):
    loc: str = Field(description="城市名称")


@tool(args_schema=WeatherQuery)
def get_weather(loc: str):
    """
        查询即时天气函数
        :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称，\
        :return：心知天气 API查询即时天气的结果，具体URL请求地址为："https://api.seniverse.com/v3/weather/now.json"
        返回结果对象类型为解析之后的JSON格式对象，并用字符串形式进行表示，其中包含了全部重要的天气信息
    """
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key": "SuN1WD2-UBwjTCODF",
        "location": loc,
        "language": "zh-Hans",
        "unit": "c",
    }
    response = requests.get(url, params=params)
    temperature = response.json()
    return temperature['results'][0]['now']


model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

tools = [get_weather]
agent = create_react_agent(model=model, tools=tools)

# response = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "你好请你介绍一下你自己"
#             }
#         ]
#     }
# )
#
# print(response)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "北京现在的天气如何?"
            }
        ]
    }
)

print(response)