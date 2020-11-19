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
            'user_code',
            'story_source',
            'story_date',
            'story_link', 
            'story_title', 
            'news_topics', 
            'who',
            'what',
            'where',
            'why', 
            'when',
            'confidence'
        ]
        return

    def put(self, data):
        table = self.dynamodb.Table(self.tableName)
        print(table)
        validData = self.getBind(data)
        
        if not len(self.errors):
            expression = 'set ';
            expressionAttributes = {}
            divider = '';
            for key in validData.keys():
                expressionAttributes[':' + key] = validData[key]
                expression += divider + key + ' = :' + key
                divider = ', '
            response = table.update_item(
                Key={
                    'user_code': validData['user_code'],
                    'story_link': validData['story_link']
                },
                UpdateExpression = "set " + expression,
                ExpressionAttributeValues = validData,
                ReturnValues = "UPDATED_NEW"
            );
            return  {
                "statusCode": 200,
                "body": json.dumps(response)
            }
            
        data['errors'] = '<br>'.join(self.errors)
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
        validData['environment'] = str(os.environ['ENVIRONMENT_NAME'])

        for attribute in self.attributes:
            if (attribute not in data.keys()) or not data[attribute]:
                self.errors.append(attribute[0].upper() + attribute[1:] + ' is required.')
            else:
                validData[attribute] = str(data[attribute])

        return validData
