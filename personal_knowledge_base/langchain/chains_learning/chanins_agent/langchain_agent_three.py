from langchain_classic.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(tavily_api_key="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", max_results=2)

tools = [search]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一名助人为乐的助手，并且可以调用工具进行网络搜索，获取实时信息。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# 初始化模型
# 使用 通义千问 模型
model = init_chat_model(
    model="qwen-plus",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
res=agent_executor.invoke({"input": "请问苹果2025WWDC发布会召开的时间是？"})
print(res)
