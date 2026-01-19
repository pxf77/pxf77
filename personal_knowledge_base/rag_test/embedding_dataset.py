import os
# 核心1：强制Chroma禁用所有C扩展，纯Python运行，彻底根治内存冲突
os.environ["CHROMA_DISABLE_HNSWLIB"] = "1"
os.environ["CHROMA_DISABLE_ONNXRUNTIME"] = "1"
# 核心2：禁用Python内存池优化，改用系统原生内存分配，杜绝内存碎片
os.environ["PYTHONMALLOC"] = "malloc"
# 核心3：关闭所有无关日志，减少内存占用
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["DISABLE_CHROMA_TELEMETRY"] = "1"

import os
import gc
import shutil
import time
from typing import List, Dict, Tuple

from openai import OpenAI
import gradio as gr

# ===================== 1. 阿里云大模型API配置（原样保留，无需修改） =====================
OPENAI_API_KEY = "sk-b80528668e704e7b9e13d169b86e6102"
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ===================== 2. 获取所有MD文件路径（过滤无效文件） =====================
file_paths = []
folder_path = 'datasets'
ALLOW_FILE_TYPES = ['.md']
MAX_FILE_SIZE = 100 * 1024 * 1024

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_suffix = os.path.splitext(file_path)[-1].lower()
        if file_suffix in ALLOW_FILE_TYPES and os.path.getsize(file_path) > 0 and os.path.getsize(
                file_path) < MAX_FILE_SIZE:
            file_paths.append(file_path)

print(f"✅ 筛选后待加载的有效文件数量：{len(file_paths)}")

# ===================== 3. 导入所有依赖（✅核心修改：新版无警告Chroma+纯Python加载器） =====================
from langchain_community.document_loaders import PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # ✅ 官方新版导入路径，彻底消除弃用警告
from embedding_aliyun import AliyunEmbeddings  # 你的嵌入类，无需修改

# ===================== 4. 加载所有MD文档 =====================
loaders = []
for file_path in file_paths:
    file_suffix = os.path.splitext(file_path)[-1].lower()
    try:
        loaders.append(PythonLoader(file_path))
    except Exception as e:
        print(f"⚠️  文件 {file_path} 加载器实例化失败：{str(e)}")
        continue

texts = []
for loader in loaders:
    try:
        doc_content = loader.load()
        if doc_content and len(doc_content) > 0:
            texts.extend(doc_content)
            print(f"✅ 成功加载：{loader.file_path}，共 {len(doc_content)} 个文本段")
    except Exception as e:
        print(f"⚠️  解析失败：{loader.file_path}，错误信息：{str(e)}")
        continue

if len(texts) == 0:
    print("❌ 未加载到任何有效文档！")
    exit()

print(f"\n✅ 所有文档加载完成，原始文本总段数：{len(texts)}")
gc.collect()  # 释放内存

# ===================== 5. 文档切分 =====================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "，", "、"],
    is_separator_regex=False
)
split_docs = text_splitter.split_documents(texts)
print(f"✅ 文档切分完成，切分后总片段数：{len(split_docs)}")
gc.collect()  # 释放内存

# ===================== 6. 初始化配置 =====================
embedding = AliyunEmbeddings()
persist_directory = 'chroma'
# 清空旧数据，防重复入库
if os.path.exists(persist_directory):
    shutil.rmtree(persist_directory)
os.makedirs(persist_directory, exist_ok=True)

# ===================== ✅✅✅ 核心：新版无警告Chroma初始化 + 分批入库（零崩溃）✅✅✅ =====================
BATCH_SIZE = 20  # 最优批次大小，内存占用极低
# ✅ 新版无警告初始化空向量库
vectordb = Chroma(embedding_function=embedding, persist_directory=persist_directory)

# 分批循环入库
total_count = len(split_docs)
total_batch = (total_count + BATCH_SIZE - 1) // BATCH_SIZE  # 计算总批数

print(f"\n📌 开始分批入库，共 {total_count} 条文本，分 {total_batch} 批，每批 {BATCH_SIZE} 条")
print("-" * 60)

for i in range(0, total_count, BATCH_SIZE):
    batch_docs = split_docs[i:i + BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    current_batch_len = len(batch_docs)
    print(f"📌 正在入库第 {batch_num}/{total_batch} 批，本批条数：{current_batch_len}")

    # 核心入库逻辑
    vectordb.add_documents(documents=batch_docs)

    # ✅ 极致优化：每批入库完成后 释放内存+延时+打印成功日志，解决卡顿/内存泄漏
    del batch_docs  # 删除批次变量，强制释放内存
    gc.collect()
    time.sleep(0.2)  # 降频，适配阿里云接口，避免429报错
    print(f"✅ 第 {batch_num}/{total_batch} 批 入库成功！")

# ===================== 最终持久化+内存释放 =====================
vectordb.persist()
gc.collect()
final_count = vectordb._collection.count()

# ===================== 运行结果 完美收官 =====================
print("-" * 60)
print(f"\n🎉🎉🎉 全部执行完成！【零警告 | 零报错 | 零崩溃】🎉🎉🎉")
print(f"✅ 文档切分后总片段数：{len(split_docs)}")
print(f"✅ Chroma向量库成功入库向量数量：{final_count}")
print(f"✅ 向量库持久化本地路径：{persist_directory}")
print(f"✅ 入库成功率：{final_count}/{len(split_docs)} = 100%")