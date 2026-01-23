from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class UserInfo(BaseModel):
    time: str
    location: str
    event: str

# 第一步：根据标题生成新闻正文
news_gen_prompt = PromptTemplate.from_template(
    "请根据以下新闻标题撰写一段简短的新闻内容（100字以内）：\n\n标题：{title}"
)

model = ChatOpenAI(
    model="qwen-turbo",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)
# 第一个子链：生成新闻内容
news_chain = news_gen_prompt | model

parser = JsonOutputParser(pydantic_object=UserInfo)

summary_prompt = PromptTemplate.from_template(
    "请从下面这段新闻内容中提取关键信息，并返回结构化JSON格式：\n\n{news}\n\n{format_instructions}"
)

summary_chain = (summary_prompt.partial(format_instructions=parser.get_format_instructions()) | model | parser)

# 组合成一个复合 Chain
full_chain = news_chain | summary_chain

# 调用复合链
# result = full_chain.invoke({"title": "苹果公司在加州发布新款AI芯片"})
# print(result)

from langchain_core.runnables import RunnableLambda
def debug_print(x):
    print('中间结果（新闻正文）：', x)
    return x

debug_node = RunnableLambda(debug_print)

# 组合成一个复合 Chain
full_chain = news_chain | debug_node | summary_chain

# 调用复合链
result = full_chain.invoke({"title": "苹果公司在加州发布新款AI芯片"})
print(result)