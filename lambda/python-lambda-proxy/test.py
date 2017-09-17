import json
import requests

def response(code):
    return {
        'statusCode': code,
        'headers': { 'Content-Type': 'application/json' }
    }

def handler(event, context):
    body = event.get('body')
    if not body:
        body = event
    else:
        body = json.loads(event['body'])


    if len(body) == 2:
        name = body.get('name')
        age = body.get('age')
        if not isinstance(name, (str, unicode)):
            return response(406)
        if not isinstance(age, int):
            return response(406)
        ''' requests.post('http://httpbin.org/post', data=event)
        post data to the elk endpoint '''
        return response(202)
    return response(400)
