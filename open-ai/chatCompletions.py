import requests
import json
from config.config import *
from utills.restUtils import printStreamResponse

requestBody = {"messages": [{
    "content": "你是洛城小助手，是洛城科技有限公司开发的。你是一个运行于用户Mac上，可以根据用户指令，并可以根据需要调用工具的AI助手。\n/no_think",
    "role": "system"}, {"content": "你是谁", "role": "user"},
], "model": "qwen-plus", "stream": True, "temperature": 0.5}


def printOpenAiResponse(response):
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data:'):
                data = decoded_line[6:]
                if data != '[DONE]':
                    json_data = json.loads(data)
                    print(
                        json_data
                        ['choices']
                        [0]
                        ['delta'].get('content', ''),
                        end=''
                    )


if __name__ == '__main__':
    response = requests.post(baseUrl + '/compatible-mode/v1/chat/completions', headers=headers,
                             json=requestBody,
                             stream=True)
    printStreamResponse(response)
