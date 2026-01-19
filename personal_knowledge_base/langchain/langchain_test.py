OPENAI_API_KEY = "sk-b80528668e704e7b9e13d169b86e6102"
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo"
)
llm
from langchain_core.prompts import ChatPromptTemplate

template = "你是一个翻译助手，可以帮助我将 {input_language} 翻译成 {output_language}."
human_template = "{text}"

chat_prompt = ChatPromptTemplate([
    ("system", template),
    ("human", human_template),
])

text = "我带着比身体重的行李，\
游入尼罗河底，\
经过几道闪电 看到一堆光圈，\
不确定是不是这里。\
"
messages  = chat_prompt.invoke({"input_language": "中文", "output_language": "英文", "text": text})
output  = llm.invoke(messages)
# print(output.model_dump_json(indent=2, ensure_ascii=False))

from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
output_parser.invoke(output)

chain = chat_prompt | llm | output_parser
output_chain = chain.invoke({"input_language":"中文", "output_language":"英文","text": text})
# print(output_chain)

text = 'I carried luggage heavier than my body and dived into the bottom of the Nile River. After passing through several flashes of lightning, I saw a pile of halos, not sure if this is the place.'
output_chain_two = chain.invoke({"input_language": "英文", "output_language": "中文","text": text})
print(output_chain_two)