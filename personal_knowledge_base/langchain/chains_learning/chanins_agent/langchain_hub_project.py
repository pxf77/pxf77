from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_classic import hub
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_classic.chat_models import init_chat_model

# 初始化 PlayWright 浏览器
sync_browser = create_sync_playwright_browser() # 创建同步执行浏览器
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser) # 构建PlayWright浏览器工具
tools = toolkit.get_tools() # 获取PlayWright浏览器操作函数

# 初始化模型
# 使用 通义千问 模型
model = init_chat_model(
    model="qwen-plus",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

# 通过 LangChain Hub 拉取提示词模版
prompt = hub.pull("hwchase17/openai-tools-agent")

# 通过 LangChain 创建 OpenAI 工具代理
agent = create_openai_tools_agent(model, tools, prompt)

# 通过 AgentExecutor 执行代理
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    # 定义任务
    command = {
        "input": "访问这个网站 https://www.microsoft.com/en-us/microsoft-365/blog/2025/01/16/copilot-is-now-included-in-microsoft-365-personal-and-family/?culture=zh-cn&country=cn 并帮我总结一下这个网站的内容"
    }

    # 执行任务
    response = agent_executor.invoke(command)
    print(response)