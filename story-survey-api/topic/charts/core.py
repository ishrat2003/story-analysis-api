import os, datetime
from .topics import Topics
from .base import Base
from reader.analysis import Analysis

class Core(Base):
    
    def __init__(self, params):
        self.dataDates = {
            'max': None,
            'min': None
        }
        self.params = params
        self.charts = {}
        self.storyAnalysis = Analysis()
        self.data = None
        self.subItemLimit = 5
        return
    
    def load(self):
        self.data = self.storyAnalysis.getTopics()
        self.charts = {}
        self.loadDataDates()
        self.setStart()
        self.setEnd()
        self.countTopics()
        self.charts['countries'] = self.storyAnalysis.getCountries()
        if self.charts['countries']:
            self.charts['countries'] = self.sort(self.charts['countries'], 'block_count')
        people = self.storyAnalysis.getPeople()
        if people:
            self.charts['people'] = self.infoPerDateRange(people, self.dataDates['start'], self.dataDates['end'])
            
        organizations = self.storyAnalysis.getOrganizations()
        if people:
            self.charts['organizations'] = self.infoPerDateRange(organizations, self.dataDates['start'], self.dataDates['end'])
        return
    
    def get(self):
        self.charts['dates'] = self.dataDates
        return self.charts
    
    def countTopics(self):
        topicsProcessor = Topics()
        self.charts['topics'] = topicsProcessor.count(self.dataDates['start'], self.dataDates['end'], self.data)
        return
    
    def loadDataDates(self):
        minYear, maxYear = self.getMaxMin(self.data.keys())
        minMonthOfMinYear, _ = self.getMaxMin(self.data[minYear].keys())
        _, maxMonthOfMaxYear = self.getMaxMin(self.data[maxYear].keys())
        minDayOfminMonthOfMinYear, _ = self.getMaxMin(self.data[minYear][minMonthOfMinYear].keys())
        _, maxDayOfMaxMonthOfMaxYear = self.getMaxMin(self.data[maxYear][maxMonthOfMaxYear].keys())
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
    
    def infoPerDateRange(self, items, start, end):
        if not items.keys():
            return []
        
        start = self.strToDate(start)
        end = self.strToDate(end)
        
        itemsInRange = {}
        
        for key in items.keys():
            keyCount = 0
            if len(items[key]['count_per_day']):
                for dateKey in items[key]['count_per_day'].keys():
                    itemDate = self.strToDate(dateKey)
                    if (itemDate >= start) and (itemDate <= end):
                        keyCount += items[key]['count_per_day'][dateKey]
                        
            if keyCount:
                itemsInRange[key] = items[key]
                itemsInRange[key]['total_block_count_in_range'] = keyCount
                
        if not itemsInRange.keys():
            return []
        
        sortedItems = self.sort(itemsInRange, 'total_block_count_in_range')
        return sortedItems[0: self.subItemLimit]
