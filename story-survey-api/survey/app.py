import json
from db.survey_item import SurveyItem

def save_handler(event, context):
    eventData = json.loads(event['body'])
    print(eventData)
    survey = SurveyItem()
    result = survey.save(eventData)
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Request-Method': '*',
            'Access-Control-Request-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "result": result
        })
    }
