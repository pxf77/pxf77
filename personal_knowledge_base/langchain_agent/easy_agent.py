# ========== 关键修改1：替换模型导入（Claude → 通义千问） ==========
from langchain_dashscope import ChatDashScope  # 通义千问的LangChain集成类
# 保留原有导入（Tavily/LangGraph部分不变）
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
import os

# ========== 关键修改2：配置通义千问+Tavily的API密钥 ==========
# 通义千问API Key（替换为你自己的）
os.environ["DASHSCOPE_API_KEY"] = "sk-b80528668e704e7b9e13d169b86e6102"
# Tavily API Key（替换为你自己的）
os.environ["TAVILY_API_KEY"] = "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"

# Create the agent
memory = MemorySaver()

# ========== 关键修改3：初始化通义千问模型（替换Claude） ==========
# 千问模型可选：qwen-turbo（轻量版）、qwen-plus（增强版）、qwen-max（旗舰版）
model = ChatDashScope(
    model_name="qwen-turbo",  # 推荐先用免费的qwen-turbo测试
    temperature=0.7,  # 随机性参数，按需调整
)

# 保留原有Tavily搜索逻辑（无需改动）
search = TavilySearch(max_results=2)
tools = [search]

# 保留原有Agent创建逻辑（LangGraph自动适配通义千问）
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent（调用逻辑完全不变）
config = {"configurable": {"thread_id": "abc123"}}
# 第一轮对话：自我介绍
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
):
    print(chunk)
    print("----")

# 第二轮对话：查询所在地天气（触发Tavily搜索）
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
):
    print(chunk)
    print("----")