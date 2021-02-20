# import sys
# packagesPath = "/opt/dependencies"
# sys.path.append(packagesPath)

import json
import nltk
nltk.data.path.append("/var/task/resources/nltkData")
from topic.local_topic import LocalTopic
from story.lc_story import LCStory
from loader.bbc import BBC

def getEventData(event):
    eventData = json.loads(event['body'])
    keys = eventData.keys()
    if ('title' not in keys) or ('content' not in keys):
        if (('source' in keys) and ('key' in keys) and (eventData['source'] == 'bbc')):
            loader = BBC()
            eventData = loader.fetchPage("https://www.bbc.co.uk/news/" + eventData['key'])
    return eventData

def lambda_lc_handler(event, context):
    concepts = {};
    eventData = getEventData(event)
    keys = eventData.keys()
    if ('title' in keys) and ('content' in keys) and('pubDate' in keys):
        localStory = LCStory()
        concepts = localStory.getConcepts(eventData['title'] + '.' + eventData['content'], eventData['pubDate']);
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Request-Method': '*',
            'Access-Control-Request-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        "body": json.dumps({
            "concepts": concepts,
            "content": eventData['content']
        })
    }
