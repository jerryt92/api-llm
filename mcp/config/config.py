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
sseEndpoint = '/c0d439f3be7e4d/sse/'
# 此处填入1session.py返回的sessionId
sessionId = '445873c4d7f74807bd7746746aee8387'
headers = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "MCP-Protocol-Version": "2025-03-26",
}
