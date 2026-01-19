import os
file_paths = []
folder_path = 'datasets'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)
print(file_paths[:3])

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# 遍历文件路径并把实例化的loader存放在loaders里
loaders = []

for file_path in file_paths:
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file_path))
    elif file_type == 'md':
        loaders.append(UnstructuredMarkdownLoader(file_path))

# 下载文件并存储到text
texts = []

for loader in loaders: texts.extend(loader.load())
text = texts[1]
print(f"每一个元素的类型：{type(text)}.",
    f"该文档的描述性数据：{text.metadata}",
    f"查看该文档的内容:\n{text.page_content[0:]}",
    sep="\n------\n")
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 切分文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50)

split_docs = text_splitter.split_documents(texts)
from zhipuai_embedding import ZhipuAIEmbeddings
embedding = ZhipuAIEmbeddings()
persist_directory = 'chroma'
from langchain_community.vectorstores import Chroma

vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)
# print(f"向量库中存储的数量：{vectordb._collection.count()}")

question="什么是大语言模型"

# sim_docs = vectordb.similarity_search(question,k=3)
# print(f"检索到的内容数：{len(sim_docs)}")
#
# for i, sim_doc in enumerate(sim_docs):
#     print(f"检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")

mmr_docs = vectordb.max_marginal_relevance_search(question,k=3)
for i, sim_doc in enumerate(mmr_docs):
    print(f"MMR 检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")

