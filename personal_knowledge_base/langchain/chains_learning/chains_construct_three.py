from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    age: int

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

parser = JsonOutputParser(pydantic_object=UserInfo)

prompt = PromptTemplate.from_template(
    "请根据以下内容提取用户信息，并返回 JSON 格式：\n{input}\n\n{format_instructions}"
)

chain = prompt.partial(format_instructions=parser.get_format_instructions()) | model | parser
print(chain.invoke({"input": "用户叫李雷，今年25岁，是一名工程师。"}))

