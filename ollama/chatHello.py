import json

import requests

from config.config import *
from utills.restUtils import printStreamResponse

requestBody = {
    "model": "qwen3:14b-q8_0", "messages": [
        {
            "role": "user",
            "content": "Hello, world!"
        }
    ],
    "stream": True,
    "keepAlive": "3600",
    "options": {"temperature": 0.5, "num_ctx": 32768}
}


def printOllamaResponse(response):
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line)
            print(
                json_data
                ['message']
                .get('content', ''),
                end=''
            )


if __name__ == '__main__':
    response = requests.post(baseUrl + '/api/chat', headers=headers, json=requestBody, stream=True)
    printStreamResponse(response)
