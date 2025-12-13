import requests
import json
from config.config import *
from utills.restUtils import printStreamResponse

# requestBody = {
#     "model": "qwen3:14b",
#     "messages": [
#         {
#             "content": "你名字叫“Jrag AI”\n/no_think",
#             "role": "system"
#         },
#         {
#             "content": "你是谁？你能做什么？",
#             "role": "user"
#         }
#     ],
#     "options": {
#         "temperature": 0.1,
#         "num_ctx": 32768
#     },
#     "stream": True,
#     "keepAlive": 3600
# }
requestBody = {"model": "qwen3:14b-q8_0", "messages": [{"role": "system",
                                                   "content": "你是Jrag AI，你是一个运行于用户Mac上，可以根据用户指令，并可以根据需要调用工具的AI助手。\n/no_think"},
                                                  {"role": "user", "content": "我电脑的磁盘空间是多少\n\n"}],
               "stream": True, "keepAlive": "3600", "tools": [{"type": "function",
                                                               "function": {"name": "execute_mac_os_shell",
                                                                            "description": "Executes any macOS shell command and returns the output.",
                                                                            "parameters": {"properties": {"command": {
                                                                                "description": "The macOS zsh command to execute.",
                                                                                "type": "string"}}, "type": "object",
                                                                                           "required": []}}},
                                                              {"type": "function",
                                                               "function": {"name": "view_website_content",
                                                                            "description": "访问传入的URL，返回解析出的网页内容",
                                                                            "parameters": {"properties": {
                                                                                "url": {"description": "website url",
                                                                                        "type": "string"}},
                                                                                           "type": "object",
                                                                                           "required": []}}},
                                                              {"type": "function", "function": {
                                                                  "name": "search_code_questions_from_internet",
                                                                  "description": "调用搜索编程相关问题，返回最多5条结果条目。",
                                                                  "parameters": {"properties": {
                                                                      "query": {"description": "Search query",
                                                                                "type": "string"}}, "type": "object",
                                                                                 "required": []}}}],
               "options": {"temperature": 0.5, "num_ctx": 32768}}


# requestBody = {"model": "qwen3:14b", "messages": [{"role": "system",
#                                                    "content": "你是Jrag AI，你是一个运行于用户Mac上，可以根据用户指令，并可以根据需要调用工具的AI助手。\n/no_think"},
#                                                   {"role": "user", "content": "我电脑的磁盘空间是多少"},
#                                                   {"role": "assistant", "content": "", "tool_calls": [{"function": {
#                                                       "name": "execute_mac_os_shell",
#                                                       "arguments": {"command": "df -h"}}}]}, {"role": "tool",
#                                                                                               "content": "ToolResponseMessage{responses=[FunctionCallingModel.ToolResponse(name=execute_mac_os_shell, responseData=Filesystem            Size    Used   Avail Capacity iused ifree %iused  Mounted on\n/dev/disk3s1s1       926Gi    10Gi   242Gi     5%    426k  2.5G    0%   /\ndevfs                349Ki   349Ki     0Bi   100%    1.2k     0  100%   /dev\n/dev/disk3s6         926Gi   3.0Gi   242Gi     2%       2  2.5G    0%   /System/Volumes/VM\n/dev/disk3s2         926Gi   6.7Gi   242Gi     3%    1.4k  2.5G    0%   /System/Volumes/Preboot\n/dev/disk3s4         926Gi   8.1Mi   242Gi     1%     106  2.5G    0%   /System/Volumes/Update\n/dev/disk1s2         500Mi   6.0Mi   476Mi     2%       1  4.9M    0%   /System/Volumes/xarts\n/dev/disk1s1         500Mi   6.8Mi   476Mi     2%      36  4.9M    0%   /System/Volumes/iSCPreboot\n/dev/disk1s3         500Mi   6.8Mi   476Mi     2%     101  4.9M    0%   /System/Volumes/Hardware\n/dev/disk3s5         926Gi   663Gi   242Gi    74%    4.6M  2.5G    0%   /System/Volumes/Data\nmap auto_home          0Bi     0Bi     0Bi   100%       0     0     -   /System/Volumes/Data/home\n/dev/disk7s1         931Gi   818Gi   113Gi    88%    3.5M  1.2G    0%   /Volumes/TimeMachine\nOrbStack:/OrbStack   244Gi    14Gi   230Gi     6%       0     0     -   /Users/tjl/OrbStack\n\nExecution completed successfully.)], messageType=tool}"}],
#                "stream": True, "keepAlive": "3600", "options": {"temperature": 0.5, "num_ctx": 32768}}


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
