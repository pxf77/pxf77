import os
from typing import List
from langchain_core.embeddings import Embeddings
from openai import OpenAI

# ===================== 你的阿里云配置（原样保留，不用改） =====================
# 阿里云DashScope的API-KEY 替换成你自己的
os.environ["OPENAI_API_KEY"] = "sk-b80528668e704e7b9e13d169b86e6102"
# 阿里云DashScope的OpenAI兼容接口地址
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class AliyunEmbeddings(Embeddings):
    """阿里云通义千问 Embedding 封装类 ✅【完整版修复】内置自动分批，适配新版LangChain"""

    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=API_BASE
        )
        self.model = "text-embedding-v4"  # 你的嵌入模型版本
        self.MAX_BATCH_SIZE = 10  # 阿里云硬性限制：单次最多请求10条文本，固定死！

    def embed_query(self, text: str) -> List[float]:
        """【单文本嵌入】- 查询向量库时调用，原有逻辑不变，无需修改"""
        if not text.strip():
            return [0.0] * 1024  # 空文本返回全0向量，避免报错
        response = self.client.embeddings.create(
            model=self.model,
            input=[text]
        )
        return response.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """【批量文本嵌入】✅ 核心修复：内置自动分批请求逻辑，根治400报错
        :param texts: 任意长度的文本列表（切分后的文档）
        :return: 所有文本对应的向量列表，顺序与输入一致
        """
        all_embeddings = []
        # 核心：循环分批处理，步长=self.MAX_BATCH_SIZE=10
        for start_idx in range(0, len(texts), self.MAX_BATCH_SIZE):
            # 切片：从start_idx开始，取最多10条文本，最后一批不足10条也没关系
            batch_texts = texts[start_idx: start_idx + self.MAX_BATCH_SIZE]
            # 过滤掉空文本，避免阿里云接口返回无效结果
            batch_texts = [txt.strip() for txt in batch_texts if txt.strip()]
            if not batch_texts:
                continue
            # 调用阿里云Embedding接口，请求当前批次的向量
            response = self.client.embeddings.create(
                model=self.model,
                input=batch_texts
            )
            # 提取当前批次的向量结果，按顺序拼接
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings
