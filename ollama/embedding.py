from config.config import *
from utills.restUtils import *

requestBody = {
    "model": "nomic-embed-text:latest",
    "input": [
        "Hello Milvus",
    ]
}

if __name__ == '__main__':
    response = requests.post(baseUrl + '/api/embed', headers=headers, json=requestBody)
    printResponse(response, pretty=False, curlInfo=True)
    json_body = response.json()
    response = json.dumps(json_body)
    dimension = len(json_body['embeddings'][0])
    print(f"dimension: {dimension}")
