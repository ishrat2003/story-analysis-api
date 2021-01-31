import json
from .s3 import S3    

class Analysis(S3):
    
    def getRcFileContent(self, key):
        content = self.getContent('words/' + key + '.json')
        if content:
            content = json.load(content['Body'])
            return content
        return None
        


