import requests

from config.config import *
from utills.restUtils import printStreamResponse

requestBody = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": 'py-mcp-test',
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {
            "sampling": {},
            "roots": {"listChanged": True}
        },
        "clientInfo": {
            "name": "Spring AI MCP Client",
            "version": "0.3.1"
        }
    }
}

if __name__ == '__main__':
    response = requests.post(baseUrl + '/messages/?session_id=' + sessionId, headers=headers,
                             json=requestBody, stream=False)
    printStreamResponse(response, pretty=True)
