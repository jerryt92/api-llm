import json

import requests


def printStreamResponse(response, pretty=True):
    print('\n' + response.request.method + ' ' + response.request.url + '\n')
    print('Request:\n')
    print('Headers:', json.dumps(dict(response.request.headers), indent=2 if pretty else None))
    request_body = response.request.body
    if isinstance(request_body, bytes):
        try:
            request_body = json.loads(request_body.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            request_body = request_body.decode('utf-8', errors='replace')

    print('Body:', json.dumps(request_body, indent=2 if pretty else None, ensure_ascii=False))
    print()
    print('Response:\n')
    print('Status Code: %s' % response.status_code)
    headersDict = dict(response.headers)
    print('Headers:', json.dumps(headersDict, indent=2 if pretty else None, ensure_ascii=False))
    print('Events:')
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)


def printResponse(response: requests.Response, pretty=True):
    print('\n' + response.request.method + ' ' + response.request.url + '\n')
    print('Request:\n')
    print('Headers:', json.dumps(dict(response.request.headers), indent=2 if pretty else None))
    request_body = response.request.body
    if isinstance(request_body, bytes):
        try:
            request_body = json.loads(request_body.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            request_body = request_body.decode('utf-8', errors='replace')

    print('Body:', json.dumps(request_body, indent=2 if pretty else None, ensure_ascii=False))
    print()
    print('Response:\n')
    print('Status Code: %s' % response.status_code)
    headersDict = dict(response.headers)
    print('Headers:', json.dumps(headersDict, indent=2 if pretty else None, ensure_ascii=False))
    try:
        json_body = response.json()
        print('Body:', json.dumps(json_body, indent=2 if pretty else None, ensure_ascii=False))
    except ValueError:
        print('Body:', response.text)
