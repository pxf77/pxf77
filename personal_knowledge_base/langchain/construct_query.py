import sys
import os
target_dir = r"/tmp/pycharm_project_509/personal_knowledge_base/rag_test"
# 把目标文件夹添加到系统路径，Python就能检索到这个目录下的所有.py文件
sys.path.append(target_dir) # 将父目录放入系统路径中

# 使用智谱 Embedding API，注意，需要将上一章实现的封装代码下载到本地
from zhipuai_embedding import ZhipuAIEmbeddings

from langchain_community.vectorstores import Chroma
zhipuai_api_key = "5e48e5172a4646e59248bc9f43a50ca8.Qp4ftnpHbrOORroJ"

embedding = ZhipuAIEmbeddings()

# 向量数据库持久化路径
persist_directory = 'chroma'

# 加载数据库
vectordb = Chroma(
    persist_directory=persist_directory,  # 允许我们将persist_directory目录保存到磁盘上
    embedding_function=embedding
)

# print(f"向量库中存储的数量：{vectordb._collection.count()}")

question = "什么是prompt engineering?"
retriever = vectordb.as_retriever(search_kwargs={"k": 3})
docs = retriever.invoke(question)
print(f"检索到的内容数：{len(docs)}")

for i, doc in enumerate(docs):
    print(f"检索到的第{i}个内容: \n {doc.page_content}", end="\n-----------------------------------------------------\n")

