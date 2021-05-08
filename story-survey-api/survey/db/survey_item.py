import os, re
import boto3
import uuid
from datetime import datetime
import socket
import json
from botocore.exceptions import ClientError

class SurveyItem:

    def __init__(self):
        self.endPointUrl = os.environ['DYNAMODB_ENDPOINT']
        if os.environ['ENVIRONMENT_NAME'] == 'local':
            self.endPointUrl = os.environ['DEFAULT_DYNAMODB_ENDPOINT']

        self.tableName = os.environ['TABLE_NAME']
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=self.endPointUrl)
        # print(self.dynamodb.tables.all())
        self.errors = []
        self.keyAttributes = ['story_link', 'user_code']
        self.attributes = [
            'id',
            'created',
            'survey_type',
            'condition',
            'environment',
            'user_code',
            'gender',
            'experiment_date_datepicker',
            'agreed',
            'level',
            'department',
            'dob_datepicker',
            'disability',
            'story_source',
            'story_date',
            'open_timestamp',
            'open_date_time',
            'close_timestamp',
            'close_date_time',
            'time_taken_in_seconds',
            'story_link', 
            'story_title',
            'who',
            'what',
            'where_location',
            'why', 
            'when_happened',
            'summary',
            'ease'
        ]   
        return
    
    def save(self, data):
        validData = self.getBind(data)
        print(validData)
        if len(self.errors):
            return { 'errors': '<br>'.join(self.errors) }
            
        if self.get(data):
            return self.update(validData)
        
        return self.create(validData)

    def get(self, data):
        response = {}
        table = self.dynamodb.Table(self.tableName)
        if not data["user_code"] or not data["story_link"]:
            return None
        try:
            response = table.scan(
                FilterExpression = 'user_code = :user_code and story_link = :story_link',
                ExpressionAttributeValues = {
                    ":user_code": data["user_code"],
                    ":story_link": data["story_link"]
                }
            )
            print(response['Items'])
            if response['Items'] and len(response['Items']):
                return response['Items'][0]['id']
        except ClientError as e:
            print(e.response['Error']['Message'])
            return None
          
        return None
        
    def create(self, data): 
        table = self.dynamodb.Table(self.tableName)
        response = {}
        try:
            response = table.put_item(Item = data)
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message']) 
            return {'errors': 'Failed to CREATE details.'}
    
        return {'message': 'Record saved successfully.'}

    def update(self, validData):
        table = self.dynamodb.Table(self.tableName)
        keys = { 'user_code': validData['user_code'], 'story_link': validData['story_link'] }
        del validData['user_code']
        del validData['story_link']
        
        expression = 'SET ';
        expressionAttributes = {}
        divider = '';
        for key in validData.keys():
            expressionAttributes[':' + key] = validData[key]
            expression += divider + key + ' = :' + key
            divider = ', '
        try:
            response = table.update_item(
                Key = keys,
                UpdateExpression = expression,
                ExpressionAttributeValues = expressionAttributes,
                ReturnValues = 'ALL_NEW'
            )
            print(response)
            if response: 
                return {'message': 'Record UPDATED successfully.'}
        except Exception as e:
            print(e)
            print(e.response['Error']['Message'])
            return {'errors': e.response['Error']['Message']}
          
        return {'errors': 'Failed to UPDATE details.'}
        
    def clean(self, text):
        text = re.sub(r"'", '', text)
        return text
    
    def getBind(self, data = {}):
        self.errors = []
        validData = {}
        now = datetime.now()
        validData['id'] = { "S": str(uuid.uuid4())}
        validData['created'] = { "S": str(now.strftime("%d/%m/%Y %H:%M:%S"))}
        validData['environment'] = { "S": str(os.environ['ENVIRONMENT_NAME'])}
        
        for attribute in self.attributes:
            if (attribute in ['id', 'created', 'environment']):
                continue
            
            if (attribute not in data.keys()) or not data[attribute]:
                if attribute == 'where_location':
                    self.errors.append('Where is required.')
                elif attribute == 'when_happened':
                    self.errors.append('When is required.')
                else:
                    self.errors.append(attribute[0].upper() + attribute[1:] + ' is required.')
            else:
                if (attribute in ['story_title']):
                    data[attribute] = self.clean(data[attribute])    
                
                if attribute in self.keyAttributes:
                    validData[attribute] = str(data[attribute])
                else:
                    validData[attribute] = { "S": str(data[attribute])}  

        return validData
