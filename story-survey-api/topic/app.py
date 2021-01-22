
import json
from charts.core import Core as Chart

def lambda_topic_handler(event, context):
    eventData = json.loads(event['body'])
    chartProcessor = Chart(eventData)
    chartProcessor.load()
    data = chartProcessor.get()
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


