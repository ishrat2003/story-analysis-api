import os
import boto3
import uuid
from datetime import datetime
import socket
import json

class SurveyItem:

    def __init__(self):
        self.tableName = os.environ['TABLE_NAME']
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['DYNAMODB_ENDPOINT'])
        print(self.dynamodb.tables.all())
        self.errors = []
        self.attributes = [
            'browserId', 'email', 'profession',
            'link', 'title', 'raw_text', 'context',
            'vizualization', 'vizualization_rate', 'is_visualization_useful',
            'generated_story', 'story_rate', 'is_story_useful',
            'suggested_story'
        ]
        return

    def put(self, data):
        table = self.dynamodb.Table(self.tableName)
        print(table)
        validData = self.getBind(data)
        if not len(self.errors):
            response = table.put_item(
                Item=validData
            )
            print(response)
            return  {
                "statusCode": 200,
                "body": json.dumps({'message': 'ok'})
            }
        data['errors'] = self.errors
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }

    def getBind(self, data):
        self.errors = []
        validData = {}
        now = datetime.now()
        hostname = socket.gethostname()

        validData['id'] = str(uuid.uuid4())
        validData['created'] = str(now.strftime("%d/%m/%Y %H:%M:%S"))
        validData['ip'] = str(socket.gethostbyname(hostname))
        validData['environment'] = str(os.environ['ENVIRONMENT_NAME'])

        for attribute in self.attributes:
            if ((attribute not in data.keys()) or not data[attribute]):
                self.errors.append(attribute + ' is required')
            else:
                validData[attribute] = str(data[attribute])

        return validData
