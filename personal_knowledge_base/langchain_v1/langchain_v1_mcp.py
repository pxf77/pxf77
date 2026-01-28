import asyncio

from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

model = init_chat_model(
    model="deepseek-v3.2",
    model_provider='openai',
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-b80528668e704e7b9e13d169b86e6102",
)

mcp_client = MultiServerMCPClient(
    {
        "amap-maps": {
              "command": "cmd",
              "args": [
                "/c",
                "npx",
                "-y",
                "@amap/amap-maps-mcp-server"
              ],
              "env": {
                "AMAP_MAPS_API_KEY": "a5e44a62bf94d31581b3625e4e31d331"
              },
              'transport': 'stdio'
            }
    }
)

async def get_server_tools():
    tools = await mcp_client.get_tools()
    print(f"加载了{len(tools)}: {[t.name for t in tools]}")



asyncio.run(get_server_tools())