import json
from .s3 import S3    

class Analysis(S3):
    
    def getTopics(self):
        content = self.getContent('gc/topics.json')
        print(content)
        if content:
            return json.load(content['Body'])
        return None


