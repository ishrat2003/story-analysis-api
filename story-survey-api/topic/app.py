
import json
from reader.analysis import Analysis
from charts.core import Core as Chart


def lambda_topic_handler(event, context):
    eventData = json.loads(event['body']);
    print('------------------------')
    print(eventData)
    storyAnalysis = Analysis()
    data = storyAnalysis.getTopics()
    if data:
        chartProcessor = Chart(eventData)
        chartProcessor.load(data)
        data = chartProcessor.get()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": data
        })
    }


