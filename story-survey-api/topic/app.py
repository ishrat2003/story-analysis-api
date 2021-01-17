
import json
from charts.core import Core as Chart

def lambda_topic_handler(event, context):
    eventData = json.loads(event['body'])
    chartProcessor = Chart(eventData)
    chartProcessor.load()
    data = chartProcessor.get()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": data
        })
    }


