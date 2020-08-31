# import sys
# packagesPath = "/opt/dependencies"
# sys.path.append(packagesPath)

import json
import nltk
nltk.data.path.append("/var/task/resources/nltkData")
from topic.local_topic import LocalTopic

def lambda_lc_handler(event, context):
    eventData = json.loads(event['body']);
    localTopicAnalyzer = LocalTopic()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "topics": localTopicAnalyzer.get(eventData['content'])
        })
    }
