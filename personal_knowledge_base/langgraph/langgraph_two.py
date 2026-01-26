import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_classic.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

class WeatherQuery(BaseModel):
    loc: str = Field(description="城市名称")

class WriteQuery(BaseModel):
    content: str = Field(description="需要写入文档的具体内容")

@tool(args_schema=WeatherQuery)
def get_weather(loc):
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

@tool(args_schema=WriteQuery)
def write_file(content):
    """
    将指定内容写入本地文件。
    :param content: 必要参数，字符串类型，用于表示需要写入文档的具体内容。
    :return：是否成功写入
    """
    with open('res.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    return "已成功写入本地文件。"

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

tools = [get_weather, write_file]

agent = create_react_agent(model=model, tools=tools)
# response = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "北京和杭州现在的天气如何?"
#             }
#         ]
#     }
# )
#
# print(response['messages'])

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "北京和杭州现在的天气如何?并把查询结果写入文件中"
            }
        ]
    }
)

print(response['messages'])