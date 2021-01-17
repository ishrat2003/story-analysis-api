import os, datetime

class Core:
    
    def __init__(self, params):
        self.dataDates = {
            'start': params['start'],
            'end': params['end']
        }
        self.topics = params['topics']
        if self.topics:
            self.topics = self.topics.split(',')
        self.subTopics = {}
        self.charts = {}
        return
    
    def get(self):
        self.charts = {}
        if not self.topics:
            return self.charts
        self.loadTopicLineChart()
        self.loadDocumentsHavingAllTopics()
        self.loadSubtopicsChart()
        self.loadStoryBoard()
        return self.charts
    
    
