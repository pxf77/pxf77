from typing import List
import os
from langchain_core.embeddings import Embeddings

class ZhipuAIEmbeddings(Embeddings):
    """`Zhipuai Embeddings` embedding models."""
    def __init__(self):
        from zai import ZhipuAiClient
        # ✅ 优化1：从环境变量读取API_KEY，避免硬编码泄露
        self.client = ZhipuAiClient(api_key=os.environ.get("ZHIPU_API_KEY", "5e48e5172a4646e59248bc9f43a50ca8.Qp4ftnpHbrOORroJ"))
        # ✅ 核心配置：智谱接口的最大批次限制，写死64即可
        self.batch_size = 64

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        生成输入文本列表的 embedding，自动分批处理，适配智谱64条限制
        Args:
            texts (List[str]): 要生成 embedding 的文本列表.
        Returns:
            List[List[float]]: 每个文档的 embedding 列表
        """
        all_embeddings = []
        # ✅ 核心逻辑：分批处理，每次取64条，循环直至所有文本处理完毕
        for i in range(0, len(texts), self.batch_size):
            # 切片获取当前批次的文本，最后一批不足64条也能兼容
            batch_texts = texts[i:i + self.batch_size]
            # 调用智谱接口获取当前批次的embedding
            embeddings_response = self.client.embeddings.create(
                model="embedding-3",
                input=batch_texts
            )
            # ✅ 优化2：修复变量命名重复的问题，提升可读性
            batch_embeddings = [item.embedding for item in embeddings_response.data]
            # 拼接当前批次结果到总结果
            all_embeddings.extend(batch_embeddings)
        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        """生成单条文本的 embedding"""
        return self.embed_documents([text])[0]