from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser# 导入标准输出组件
from langchain_core.output_parsers import ResponseSchema, StructuredOutputParser
import sys, langchain_core, pprint, pathlib

pprint.pp({
    "exe": sys.executable,
    "version": langchain_core.__version__,
    "file": pathlib.Path(langchain_core.__file__).resolve()
})
model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102", #你注册的硅基流动api_key
)

prompt_template = ChatPromptTemplate([
    ("system", "你是一个乐意助人的助手，请根据用户的问题给出回答"),
    ("user", "这是用户的问题： {topic}， 请用 yes 或 no 来回答")
])

# 搭建链条，把model和字符串输出解析器组件连接在一起
basic_qa_chain = prompt_template | model | StrOutputParser()
# bool类型
# bool_qa_chain = prompt_template | model | BooleanOutputParser()

# 查看输出结果
question = "请问 1 + 1 是否 大于 2？"
result = basic_qa_chain.invoke({'topic':question})
# result = bool_qa_chain.invoke({'topic': question})
print(result)

