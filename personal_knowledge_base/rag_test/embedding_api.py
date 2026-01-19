from openai import OpenAI
import gradio as gr


def openai_embedding(text: str, model: str=None):
    OPENAI_API_KEY = "sk-b80528668e704e7b9e13d169b86e6102"
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 使用阿里云大模型API
    )


    # 通义千问 text-embedding-v1 text-embedding-v2  text-embedding-v3（1024维度） text-embedding-v4（1024维度）
    if model == None:
        model = "text-embedding-v2"

    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response

response = openai_embedding(text='要生成 embedding 的输入文本，字符串形式。')
print(f'返回的embedding类型为：{response.object}')
print(f'embedding长度为：{len(response.data[0].embedding)}')
print(f'embedding（前10）为：{response.data[0].embedding[:10]}')
print(f'本次embedding model为：{response.model}')
print(f'本次token使用情况为：{response.usage}')