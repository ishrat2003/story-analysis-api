# import sys
# packagesPath = "/opt/dependencies"
# sys.path.append(packagesPath)

import json
import nltk
nltk.data.path.append("/var/task/resources/nltkData")
from topic.local_topic import LocalTopic
from story.lc_story import LCStory

def lambda_lc_handler(event, context):
    eventData = json.loads(event['body']);
    localStory = LCStory()
    concepts = localStory.getConcepts(eventData['title'] + '.' + eventData['content'], eventData['pubDate']);
    return {
        "statusCode": 200,
        "body": json.dumps({
            "concepts": concepts
        })
    }
