
import json
from storyboard.core import Core as Storyboard


def lambda_storyboard_handler(event, context):
    eventData = json.loads(event['body']);
    storyboard = Storyboard(eventData)
    data = storyboard.get()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": data
        })
    }


