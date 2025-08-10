import requests
from config.config import *
from utills.restUtils import printStreamResponse

if __name__ == '__main__':
    print(baseUrl + '/xxx/sse')
    response = requests.get(baseUrl + '/xxx/sse', headers=headers, stream=True)
    printStreamResponse(response, pretty=True)
