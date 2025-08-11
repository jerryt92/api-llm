# 例如：https://www.modelscope.cn/mcp/servers/@Joooook/12306-mcp
# 申请到的MCP Server配置为：
# {
#   "mcpServers": {
#     "12306-mcp": {
#       "type": "sse",
#       "url": "https://mcp.api-inference.modelscope.net/xxx/sse"
#     }
#   }
# }
baseUrl = 'https://mcp.api-inference.modelscope.net'
sseEndpoint = '/xxx/sse/'
# 此处填入1session.py返回的sessionId
sessionId = '6e28e0673c254d7e9060e4aae08a4ef8'
headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "MCP-Protocol-Version": "2025-03-26",
}
