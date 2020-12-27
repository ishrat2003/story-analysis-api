from __future__ import print_function
import json
import urllib
import os

class KnowledgeGraph():
    
    def __init__(self):
        self.endPoint = 'https://kgsearch.googleapis.com/v1/entities:search'
        self.apiKey = os.environ['GOOGLE_KNOWLEDGE_GRAPH']
        self.reset()
        return
    
    def reset(self):
        self.objects = {}
        self.categories = {}
        return
    
    def getObjects(self):
        return self.objects
    
    def getObjectDetails(self, key):
        if key not in self.objects.keys():
            return None
        return self.objects[key]
    
    def getCategories(self):
        return self.categories
    
    def getGraph(self):
        return {
            "nodes": [
                {
                    "name": "Peter",
                    "label": "Person",
                    "id": 1
                },
                {
                    "name": "Michael",
                    "label": "Person",
                    "id": 2
                },
                {
                    "name": "Neo4j",
                    "label": "Database",
                    "id": 3
                },
                {
                    "name": "Graph Database",
                    "label": "Database",
                    "id": 4
                }
            ],
            "links": [
                {
                    "source": 1,
                    "target": 2,
                    "type": "KNOWS",
                    "since": 2010
                },
                {
                    "source": 1,
                    "target": 3,
                    "type": "FOUNDED"
                },
                {
                    "source": 2,
                    "target": 3,
                    "type": "WORKS_ON"
                },
                {
                    "source": 3,
                    "target": 4,
                    "type": "IS_A"
                }
            ]
        };
        
    
    def addObject(self, key, query):
        params = {
            'query': query,
            'limit': 1,
            'indent': True,
            'key': self.apiKey,
        }
        url = self.endPoint + '?' + urllib.parse.urlencode(params)
        response = json.loads(urllib.request.urlopen(url).read())
        
        if not response or ('itemListElement' not in response.keys()) or not response['itemListElement'] or not response['itemListElement'][0]['result']:
            if self.isPerson(query.lower()):
                self.objects[key] = {
                    "name": query,
                    "description": "",
                    "types": [],
                    "category": "Person"
                }
                self.appendCategoryItem("Person", query)
                return True
            return False
        
        if response['itemListElement'][0]['resultScore'] < 5:
            return False
        
        category = self.getCategory(response['itemListElement'][0]['result'])
        self.objects[key] = {
            "name": query,
            "description": self.getDescription(response['itemListElement'][0]['result']),
            "types": response['itemListElement'][0]['result']['@type'],
            "category": category
        }
        self.appendCategoryItem(category, query)
        
        return True
    
    def appendCategoryItem(self, category, item):
        if category not in self.categories.keys():
            self.categories[category] = []
            
        if item not in self.categories[category]:
            self.categories[category].append(item);
        return
    
    def getDescription(self, item):
        if not item:
            return ''
        
        if 'detailedDescription' not in item.keys():
            return ''
        
        if 'articleBody' in item['detailedDescription'].keys():
            return item['detailedDescription']['articleBody']
        
        return ''
    
    def getCategory(self, result):
        types = result['@type']
        if 'Person' in types:
            return 'Person'
        
        if ('Place' in types) or ('Country' in types) or ('City' in types):
            return 'Location'
        
        if self.isTime(result):
            return 'Time'
        
        if ('Organization' in types) or ('EducationalOrganization' in types):
            return 'Organization'
        
        types.remove('Thing')
        if types:
            return types[0]
        
        return 'Others'
    
    def isTime(self, item):
        if ('description' in item.keys()) and (item["description"] in ['Day of week', 'Month']):
            return True
        if ('detailedDescription' in item.keys()) and ('articleBody' in item['detailedDescription'].keys()) and self.stringContains(item['detailedDescription']['articleBody'].lower(), 'festival'):
            return True
        return False
            
    
    def isPerson(self, text):
        for title in ['mr', 'mrs', 'miss', 'dr', 'doctor', 'prof', 'professor']:
            if self.stringContains(text, title + ' '):
                return True
            
        return False
    
    def stringContains(self, text, subText):
        if not text or (text.find(subText) == -1):
            return False
        return True
