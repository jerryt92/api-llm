import requests
from config.config import *
from utills.restUtils import printStreamResponse

requestBody = {
    "jsonrpc": "2.0",
    "id": 'py-mcp-test',
    "method": "tools/call",
    "params": {
        "name": "bing_search",
        "arguments": {
            "query": "MCP 协议",
            "num_results": 5
        }
    }
}

if __name__ == '__main__':
    response = requests.post(baseUrl + '/messages/?session_id=' + sessionId, headers=headers,
                             json=requestBody, stream=False)
    printStreamResponse(response, pretty=True)
