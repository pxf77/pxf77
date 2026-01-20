# 使用智谱 Embedding API，注意，需要将上一章实现的封装代码下载到本地
from zhipuai_embedding import ZhipuAIEmbeddings

from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import os

OPENAI_API_KEY = "sk-b80528668e704e7b9e13d169b86e6102"

# 定义 Embeddings
embedding = ZhipuAIEmbeddings()

# 向量数据库持久化路径
persist_directory = 'chroma'

# 加载数据库
vectordb = Chroma(
    persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
    embedding_function=embedding
)

# 使用 OpenAI GPT-4o 模型
llm = ChatOpenAI(api_key=OPENAI_API_KEY,
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model="qwen-turbo",
                 temperature=0)

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
template_v1 = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
{context}
问题: {question}
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template_v1)

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

retrievel_chain = vectordb.as_retriever() | RunnableLambda(combine_docs)

qa_chain = (
    RunnableParallel(context=retrievel_chain, question=RunnablePassthrough())
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# question = "什么是南瓜书"
# result = qa_chain.invoke(question)
# print(result)


template_v2 = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。你应该使答案尽可能详细具体，但不要偏题。如果答案比较长，请酌情进行分段，以提高答案的阅读体验。
{context}
问题: {question}
有用的回答:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template_v2)
qa_chain = (
    RunnableParallel(context=retrievel_chain, question=RunnablePassthrough())
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# question = "什么是南瓜书"
# result = qa_chain.invoke(question)
# print(result)
# question = "使用大模型时，构造 Prompt 的原则有哪些"
# result = qa_chain.invoke(question)
# print(result)


template_v3 = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。你应该使答案尽可能详细具体，但不要偏题。如果答案比较长，请酌情进行分段，以提高答案的阅读体验。
如果答案有几点，你应该分点标号回答，让答案清晰具体
{context}
问题: {question}
有用的回答:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                 template=template_v3)
qa_chain = (
    RunnableParallel(context=retrievel_chain, question=RunnablePassthrough())
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# question = "使用大模型时，构造 Prompt 的原则有哪些"
# result = qa_chain.invoke(question)
# print(result)

# question = "强化学习的定义是什么"
# result = qa_chain.invoke(question)
# print(result)

template_v4 = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。你应该使答案尽可能详细具体，但不要偏题。如果答案比较长，请酌情进行分段，以提高答案的阅读体验。
如果答案有几点，你应该分点标号回答，让答案清晰具体。
请你附上回答的来源原文，以保证回答的正确性。
{context}
问题: {question}
有用的回答:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                 template=template_v4)
qa_chain = (
    RunnableParallel(context=retrievel_chain, question=RunnablePassthrough())
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# question = "强化学习的定义是什么"
# result = qa_chain.invoke(question)
# print(result)

# question = "我们应该如何去构造一个LLM项目"
# result = qa_chain.invoke(question)
# # print(result)

template_v4 = """
请你依次执行以下步骤：
① 使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案。
你应该使答案尽可能详细具体，但不要偏题。如果答案比较长，请酌情进行分段，以提高答案的阅读体验。
如果答案有几点，你应该分点标号回答，让答案清晰具体。
上下文：
{context}
问题: 
{question}
有用的回答:
② 基于提供的上下文，反思回答中有没有不正确或不是基于上下文得到的内容，如果有，回答你不知道
确保你执行了每一个步骤，不要跳过任意一个步骤。
"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                 template=template_v4)
qa_chain = (
    RunnableParallel(context=retrievel_chain, question=RunnablePassthrough())
    | QA_CHAIN_PROMPT
    | llm
    | StrOutputParser()
)

# question = "我们应该如何去构造一个LLM项目"
# result = qa_chain.invoke(question)
# print(result)

# question = "LLM的分类是什么？给我返回一个 Python List"
# result = qa_chain.invoke(question)
# print(result)

# 使用第二章讲过的 OpenAI 原生接口

from openai import OpenAI

OPENAI_API_KEY = "sk-b80528668e704e7b9e13d169b86e6102"
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 使用阿里云大模型API
)


def gen_gpt_messages(prompt):
    """
    构造 GPT 模型请求参数 messages

    请求参数：
        prompt: 对应的用户提示词
    """
    messages = [{"role": "user", "content": prompt}]
    return messages


def get_completion(prompt, model="qwen-plus", temperature=0):
    """
    获取 GPT 模型调用结果

    请求参数：
        prompt: 对应的提示词
        model: 调用的模型，默认为 gpt-4o，也可以按需选择 gpt-4 等其他模型
        temperature: 模型输出的温度系数，控制输出的随机程度，取值范围是 0~2。温度系数越低，输出内容越一致。
    """
    response = client.chat.completions.create(
        model=model,
        messages=gen_gpt_messages(prompt),
        temperature=temperature,
    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"


prompt_input = '''
请判断以下问题中是否包含对输出的格式要求，并按以下要求输出：
请返回给我一个可解析的Python列表，列表第一个元素是对输出的格式要求，应该是一个指令；第二个元素是去掉格式要求的问题原文
如果没有格式要求，请将第一个元素置为空
需要判断的问题：
{}
不要输出任何其他内容或格式，确保返回结果可解析。
'''
# response = get_completion(prompt_input.format(question))
# print(response)
prompt_output = '''
请根据回答文本和输出格式要求，按照给定的格式要求对问题做出回答
需要回答的问题：
{}
回答文本：
{}
输出格式要求：
{}
'''
question = 'LLM的分类是什么？给我返回一个 Python List'
# 首先将格式要求与问题拆分
input_lst_s = get_completion(prompt_input.format(question))
# 找到拆分之后列表的起始和结束字符
start_loc = input_lst_s.find('[')
end_loc = input_lst_s.find(']')
rule, new_question = eval(input_lst_s[start_loc:end_loc+1])
# 接着使用拆分后的问题调用检索链
result = qa_chain.invoke(new_question)
result_context = result
# 接着调用输出格式解析
response = get_completion(prompt_output.format(new_question, result_context, rule))
print(response)
