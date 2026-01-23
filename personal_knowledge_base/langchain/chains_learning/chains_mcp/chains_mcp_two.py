import pandas as pd

from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool # 从LangChain依赖库引入Python代码解释器


df = pd.read_csv('global_cities_data.csv')
tool = PythonAstREPLTool(locals={"df": df}) # 传递给代码解释器的局部变量，这里是读取表格内容的pandas对象

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102", #你注册的硅基流动api_key
)

# llm_with_tools = model.bind_tools([tool]) # 将工具与大模型绑定
#
# response = llm_with_tools.invoke(
#     "我有一张表，名为'df'，请帮我计算GDP_Billion_USD字段的均值。"
# )
#
# print(response)

from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser

parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)

llm_with_tools = model.bind_tools([tool]) # 将工具与大模型绑定

# llm_chain = llm_with_tools | parser
#
# response = llm_chain.invoke(
#     "我有一张表，名为'df'，请帮我计算GDP_Billion_USD字段的均值。"
# )

# print(response)

from langchain_core.prompts import ChatPromptTemplate
# 添加提示词模板
system = f"""
你可以访问一个名为 `df` 的 pandas 数据框，你可以使用df.head().to_markdown() 查看数据集的基本信息， \
请根据用户提出的问题，编写 Python 代码来回答。只返回代码，不返回其他内容。只允许使用 pandas 和内置库。
"""

prompt = ChatPromptTemplate([
    ("system", system),
    ("user", "{question}")
])

# 在链中加入提示词组件
llm_chain = prompt | llm_with_tools | parser | tool

response = llm_chain.invoke(
    "我有一张表，名为'df'，请帮我计算GDP_Billion_USD字段的最大值是多少，并输出对应的国家。"
)
print(response)