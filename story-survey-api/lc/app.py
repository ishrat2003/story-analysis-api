# import sys
# packagesPath = "/opt/dependencies"
# sys.path.append(packagesPath)

import json
import nltk
nltk.data.path.append("/opt/nltkData")
from lc import Peripheral

def lambda_lc_handler(event, context):
    eventData = json.loads(event['body']);
    return {
        "statusCode": 200,
        "body": json.dumps({
            "contributors": eventData['title']
        }),
    }
