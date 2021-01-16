import os, datetime
from .topics import Topics

class Core:
    
    def __init__(self, params):
        # self.maxTopics = os.environ['TOPICS_LIMIT']
        self.dataDates = {
            'max': None,
            'min': None
        }
        self.params = params
        self.charts = {}
        return
    
    def load(self, data):
        self.charts = {}
        self.loadDataDates(data)
        self.setStart()
        self.setEnd()
        self.countTopics(data)
        return
    
    def get(self):
        
        self.charts['dates'] = self.dataDates
        
        return self.charts
    
    def countTopics(self, data):
        topicsProcessor = Topics()
        self.charts['topics'] = topicsProcessor.count(self.dataDates['start'], self.dataDates['end'], data)
        return
    
    def loadDataDates(self, data):
        minYear, maxYear = self.getMaxMin(data.keys())
        minMonthOfMinYear, _ = self.getMaxMin(data[minYear].keys())
        _, maxMonthOfMaxYear = self.getMaxMin(data[maxYear].keys())
        minDayOfminMonthOfMinYear, _ = self.getMaxMin(data[minYear][minMonthOfMinYear].keys())
        _, maxDayOfMaxMonthOfMaxYear = self.getMaxMin(data[maxYear][maxMonthOfMaxYear].keys())
        self.dataDates = {
            'max': maxYear + '-' + self.getFormattedMonthOrDay(maxMonthOfMaxYear) + '-' + self.getFormattedMonthOrDay(maxDayOfMaxMonthOfMaxYear),
            'min': minYear + '-' + self.getFormattedMonthOrDay(minMonthOfMinYear) + '-' + self.getFormattedMonthOrDay(minDayOfminMonthOfMinYear)
        }
        return
    
    def setStart(self):
        if (('start' not in self.params.keys()) or not self.isValidMin(self.params['start'])):
            self.dataDates['start'] = self.dataDates['min']
        else:
            self.dataDates['start'] = self.params['start']
        return
    
    def setEnd(self):
        if (('end' not in self.params.keys()) or not self.isValidMax(self.params['end'])):
            self.dataDates['end'] = self.dataDates['max']
        else:
            self.dataDates['end'] = self.params['end']
        return
    
    def isValidMin(self, date):
        date = self.strToDate(date)
        minDate = self.strToDate(self.dataDates['min'])
        return date >= minDate
    
    def isValidMax(self, date):
        date = self.strToDate(date)
        maxDate = self.strToDate(self.dataDates['max'])
        return date <= maxDate
    
    def strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def getFormattedMonthOrDay(self, number):
        if int(number) < 10:
            return '0' + number
        return number

    def getMaxMin(self, items):
        items = sorted(items)
        totalItems = len(items)
        min = items[0]
        max = items[totalItems - 1]
        return min, max