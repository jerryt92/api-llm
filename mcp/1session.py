import requests
from config.config import *
from utills.restUtils import printStreamResponse

if __name__ == '__main__':
    print(baseUrl + sseEndpoint)
    response = requests.get(baseUrl + sseEndpoint, headers=headers, stream=True)
    printStreamResponse(response, pretty=True)
