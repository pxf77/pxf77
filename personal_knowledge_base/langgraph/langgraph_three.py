from langchain_tavily import TavilySearch
from langchain_classic.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

search_tool = TavilySearch(
    max_results=5,
    topic="general",
    tavily_api_key='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'
)

tools = [search_tool]

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

search_agent = create_react_agent(model=model, tools=tools)

response = search_agent.invoke({"messages": [{"role": "user", "content": "请帮我搜索最近OpenAI CEO在访谈中的核心观点。"}]})

print(response["messages"][-1].content)