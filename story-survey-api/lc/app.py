# import sys
# packagesPath = "/opt/dependencies"
# sys.path.append(packagesPath)

import json
# import nltk
# from lc import LC
import numpy
import nltk
nltk.data.path.append("/opt/nltkData")

def lambda_lc_handler(event, context):
    eventData = json.loads(event['body']);
    return {
        "statusCode": 200,
        "body": json.dumps({
            "contributors": eventData['title']
        }),
    }
