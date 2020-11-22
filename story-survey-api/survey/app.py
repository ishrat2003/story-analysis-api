import json
from db.survey_item import SurveyItem

def save_handler(event, context):
    eventData = json.loads(event['body'])
    print(eventData)
    survey = SurveyItem()
    return survey.save(eventData)
