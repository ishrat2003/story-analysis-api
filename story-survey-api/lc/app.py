import json

def lambda_lc_handler(event, context):
    eventData = json.loads(event['body']);
    return {
        "statusCode": 200,
        "body": json.dumps({
            "contributors": eventData['title']
        }),
    }
