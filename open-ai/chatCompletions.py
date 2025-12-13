import requests
import json
from config.config import *
from utills.restUtils import printStreamResponse

requestBody = {
    "messages": [
        {
            "content": "你是Jrag AI，一个可以根据用户请求需要调用工具和检索知识的AI助手。请遵循以下指南：\n1. 必须使用支撑信息中的完整原文，禁止省略任何部分或尝试理解总结支撑信息的原文。\n2. 确保你的回答包含问题中要求的所有信息，如果文本中没有有用信息则信息在图像中，必须在回答中输出图像Markdown格式的URL。\n3. 所有可能需要调用工具的用户请求，必须先尝试调用工具。\n/no_think",
            "role": "system"
        },
        {
            "content": "查询明天武汉到上海的所有车次信息",
            "role": "user"
        },
        {
            "content": "",
            "role": "assistant",
            "tool_calls": [
                {
                    "index": 0,
                    "id": "121371609",
                    "type": "function",
                    "function": {
                        "name": "get-current-date",
                        "arguments": "[{}]"
                    }
                }
            ]
        },
        {
            "content": "{\\\"type\\\":\\\"text\\\",\\\"text\\\":\\\"2025-12-08\\\"}",
            "role": "tool",
            "tool_call_id": "121371609"
        }
    ],
    "model": "openai/gpt-oss-20b",
    "stream": True,
    "temperature": 0.5,
    "tools": [
        {
            "type": "function",
            "function": {
                "description": "查询12306中转余票信息。尚且只支持查询前十条。",
                "name": "get-interline-tickets",
                "parameters": {
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "查询日期，格式为 \"yyyy-MM-dd\"。如果用户提供的是相对日期（如“明天”），请务必先调用 `get-current-date` 接口获取当前日期，并计算出目标日期。"
                        },
                        "toStation": {
                            "type": "string",
                            "description": "出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。"
                        },
                        "latestStartTime": {
                            "type": "number",
                            "description": "最迟出发时间（0-24），默认为24。"
                        },
                        "trainFilterFlags": {
                            "type": "string",
                            "description": "车次筛选条件，默认为空。从以下标志中选取多个条件组合[G(高铁/城际),D(动车),Z(直达特快),T(特快),K(快速),O(其他),F(复兴号),S(智能动车组)]"
                        },
                        "earliestStartTime": {
                            "type": "number",
                            "description": "最早出发时间（0-24），默认为0。"
                        },
                        "limitedNum": {
                            "type": "number",
                            "description": "返回的中转余票数量限制，默认为10。"
                        },
                        "format": {
                            "type": "string",
                            "description": "返回结果格式，默认为text，建议使用text。可选标志：[text, json]"
                        },
                        "middleStation": {
                            "type": "string",
                            "description": "中转地的 `station_code` ，可选。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。"
                        },
                        "sortReverse": {
                            "type": "boolean",
                            "description": "是否逆向排序结果，默认为false。仅在设置了sortFlag时生效。"
                        },
                        "showWZ": {
                            "type": "boolean",
                            "description": "是否显示无座车，默认不显示无座车。"
                        },
                        "sortFlag": {
                            "type": "string",
                            "description": "排序方式，默认为空，即不排序。仅支持单一标识。可选标志：[startTime(出发时间从早到晚), arriveTime(抵达时间从早到晚), duration(历时从短到长)]"
                        },
                        "fromStation": {
                            "type": "string",
                            "description": "出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。"
                        }
                    },
                    "type": "object",
                    "required": [
                        "date",
                        "fromStation",
                        "toStation"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "查询特定列车车次在指定区间内的途径车站、到站时间、出发时间及停留时间等详细经停信息。当用户询问某趟具体列车的经停站时使用此接口。",
                "name": "get-train-route-stations",
                "parameters": {
                    "properties": {
                        "format": {
                            "type": "string",
                            "description": "返回结果格式，默认为text，建议使用text。可选标志：[text, json]"
                        },
                        "departDate": {
                            "type": "string",
                            "description": "列车出发的日期 (格式: yyyy-MM-dd)。如果用户提供的是相对日期，请务必先调用 `get-current-date` 解析。"
                        },
                        "trainCode": {
                            "type": "string",
                            "description": "要查询的车次 `train_code`，例如\"G1033\"。"
                        }
                    },
                    "type": "object",
                    "required": [
                        "trainCode",
                        "departDate"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "通过具体的中文车站名查询其 `station_code` 和车站名。此接口主要用于在用户提供**具体车站名**作为出发地或到达地时，为接口准备 `station_code` 参数。",
                "name": "get-station-code-by-names",
                "parameters": {
                    "properties": {
                        "stationNames": {
                            "type": "string",
                            "description": "具体的中文车站名称，例如：\"北京南\", \"上海虹桥\"。若要查询多个站点，请用|分割，比如\"北京南|上海虹桥\"。"
                        }
                    },
                    "type": "object",
                    "required": [
                        "stationNames"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "通过中文城市名查询代表该城市的 `station_code`。此接口主要用于在用户提供**城市名**作为出发地或到达地时，为接口准备 `station_code` 参数。",
                "name": "get-station-code-of-citys",
                "parameters": {
                    "properties": {
                        "citys": {
                            "type": "string",
                            "description": "要查询的城市，比如\"北京\"。若要查询多个城市，请用|分割，比如\"北京|上海\"。"
                        }
                    },
                    "type": "object",
                    "required": [
                        "citys"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "查询数据通信领域的名词，返回其介绍。任何数据通信领域的名词都必须先尝试调用这个工具尝试查询。",
                "name": "query_data_communication_encyclopedia",
                "parameters": {
                    "properties": {
                        "word": {
                            "type": "string",
                            "description": "数据通信领域的名词"
                        }
                    },
                    "type": "object",
                    "required": [
                        "word"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "获取当前日期，以上海时区（Asia/Shanghai, UTC+8）为准，返回格式为 \"yyyy-MM-dd\"。主要用于解析用户提到的相对日期（如“明天”、“下周三”），提供准确的日期输入。",
                "name": "get-current-date",
                "parameters": {
                    "properties": {},
                    "type": "object",
                    "required": []
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "通过车站的 `station_telecode` 查询车站的详细信息，包括名称、拼音、所属城市等。此接口主要用于在已知 `telecode` 的情况下获取更完整的车站数据，或用于特殊查询及调试目的。一般用户对话流程中较少直接触发。",
                "name": "get-station-by-telecode",
                "parameters": {
                    "properties": {
                        "stationTelecode": {
                            "type": "string",
                            "description": "车站的 `station_telecode` (3位字母编码)"
                        }
                    },
                    "type": "object",
                    "required": [
                        "stationTelecode"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "查询12306余票信息。",
                "name": "get-tickets",
                "parameters": {
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "查询日期，格式为 \"yyyy-MM-dd\"。如果用户提供的是相对日期（如“明天”），请务必先调用 `get-current-date` 接口获取当前日期，并计算出目标日期。"
                        },
                        "toStation": {
                            "type": "string",
                            "description": "到达地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。"
                        },
                        "latestStartTime": {
                            "type": "number",
                            "description": "最迟出发时间（0-24），默认为24。"
                        },
                        "trainFilterFlags": {
                            "type": "string",
                            "description": "车次筛选条件，默认为空，即不筛选。支持多个标志同时筛选。例如用户说“高铁票”，则应使用 \"G\"。可选标志：[G(高铁/城际),D(动车),Z(直达特快),T(特快),K(快速),O(其他),F(复兴号),S(智能动车组)]"
                        },
                        "earliestStartTime": {
                            "type": "number",
                            "description": "最早出发时间（0-24），默认为0。"
                        },
                        "limitedNum": {
                            "type": "number",
                            "description": "返回的余票数量限制，默认为0，即不限制。"
                        },
                        "format": {
                            "type": "string",
                            "description": "返回结果格式，默认为text，建议使用text与csv。可选标志：[text, csv, json]"
                        },
                        "sortReverse": {
                            "type": "boolean",
                            "description": "是否逆向排序结果，默认为false。仅在设置了sortFlag时生效。"
                        },
                        "sortFlag": {
                            "type": "string",
                            "description": "排序方式，默认为空，即不排序。仅支持单一标识。可选标志：[startTime(出发时间从早到晚), arriveTime(抵达时间从早到晚), duration(历时从短到长)]"
                        },
                        "fromStation": {
                            "type": "string",
                            "description": "出发地的 `station_code` 。必须是通过 `get-station-code-by-names` 或 `get-station-code-of-citys` 接口查询得到的编码，严禁直接使用中文地名。"
                        }
                    },
                    "type": "object",
                    "required": [
                        "date",
                        "fromStation",
                        "toStation"
                    ]
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "访问传入的URL，返回解析出的网页内容",
                "name": "view_website_content",
                "parameters": {
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "website url"
                        }
                    },
                    "type": "object",
                    "required": []
                },
                "strict": False
            }
        },
        {
            "type": "function",
            "function": {
                "description": "通过中文城市名查询该城市 **所有** 火车站的名称及其对应的 `station_code`，结果是一个包含多个车站信息的列表。",
                "name": "get-stations-code-in-city",
                "parameters": {
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "中文城市名称，例如：\"北京\", \"上海\""
                        }
                    },
                    "type": "object",
                    "required": [
                        "city"
                    ]
                },
                "strict": False
            }
        }
    ]
}


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
    response = requests.post(baseUrl + '/v1/chat/completions', headers=headers,
                             json=requestBody,
                             stream=True)
    printStreamResponse(response)
    # for line in response.iter_lines():
    #     if line:
    #         decoded_line = line.decode('utf-8')
    #         if decoded_line.startswith('data:'):
    #             data = decoded_line[6:]
    #             if data != '[DONE]':
    #                 json_data = json.loads(data)
    #                 print(
    #                     json_data
    #                     ['choices']
    #                     [0]
    #                     ['delta'].get('content', ''),
    #                     end=''
    #                 )
