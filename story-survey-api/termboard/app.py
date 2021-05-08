
import json
from termboard.core import Core as Termboard


def lambda_termboard_handler(event, context):
    eventData = json.loads(event['body']);
    print(eventData)
    termboard = Termboard(eventData)
    data = termboard.get()
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Request-Method': '*',
            'Access-Control-Request-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "data": data
        })
    }


