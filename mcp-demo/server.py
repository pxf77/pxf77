from mcp.server.fastmcp import FastMCP

# 创建MCP 服务
mcp = FastMCP('Demo')

@mcp.tool()
def add(a:int, b:int) ->int:
  """"
  计算两个整数的和并返回
  """
  return a+b

if __name__ == "__main__":
  # 以标准 I/O 方式运行 MCP 服务器
  mcp.run(transport='stdio')