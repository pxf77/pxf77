from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser # 导入标准输出组件

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102", #你注册的硅基流动api_key
)

# 搭建链条，把model和字符串输出解析器组件连接在一起
basic_qa_chain = model | StrOutputParser()

# 查看输出结果
question = "你好，请你介绍一下你自己。"
result = basic_qa_chain.invoke(question)

print(result)