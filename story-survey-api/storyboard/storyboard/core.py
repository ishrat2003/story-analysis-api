import os, datetime, operator
from reader.analysis import Analysis

class Core:
    
    def __init__(self, params):
        self.rcAnalysis = Analysis()
        self.documentLimit = 25
        self.subTopicDocumentLimit = 2
        self.topics = params['topic_keys']
        self.storyboard = {}
        self.data = None
        self.documents = {}
        self.datedCount = []
        self.scoredTopics = {}
        self.maxDate = None
        self.minDate = None
        self.load()
        return
    
    def get(self):
        if not self.data:
            return self.storyboard
        
        # self.loadTopicLineChart()
        # self.loadDocumentsHavingAllTopics()
        # self.loadSubtopicsChart()
        # self.loadStoryBoard()
        return self.storyboard
    
    def loadDocuments(self):
        if not self.data or 'documents' not in self.data.keys():
            return
        
        years = self.data['documents'].keys()
        if not len(years):
            return
        # print("years", years)
        for year in years:
            months = self.data['documents'][year].keys()
            if not len(months):
                continue
            # print("months", months)
            for month in months:
                days = self.data['documents'][year][month].keys()
                if not len(days):
                    continue
                # print("days", days)
                for day in days:
                    fullDateKey = year + '-' + self.getFormattedMonthOrDay(month) + '-' + self.getFormattedMonthOrDay(day)
                    fullDate = self.strToDate(fullDateKey)
                    self.setMaxDate(fullDate)
                    self.setMinDate(fullDate)
                    links = self.data['documents'][year][month][day].keys()
                    if not len(links):
                        self.datedCount.append({
                            "date": fullDateKey,
                            "match_count": 0
                        })
                        continue
                    
                    # print("total links(", fullDateKey, "):", len(links))
                    totalMatch = 0
                    
                    for link in links:
                        score = self.getDocumentTopicScore(self.data['documents'][year][month][day][link])
                        if score > 0:
                            totalMatch += 1
                            self.documents[link] = self.data['documents'][year][month][day][link]
                            self.documents[link]['score'] = score
                            self.documents[link]['date_key'] = fullDateKey
                            self.scoreTerms(self.documents['link'], fullDate, 'topics')
                            # self.scoreTerms(self.documents['link'], fullDate, 'actions')
                            # self.scoreTerms(self.documents['link'], fullDate, 'positive')
                            # self.scoreTerms(self.documents['link'], fullDate, 'negative')
                    
                    self.datedCount.append({
                        "date": fullDateKey,
                        "match_count": totalMatch
                    })

        if self.documents:
            sortedDocuments = self.sort(self.documents)
            # print('====== total docs:', len(sortedDocuments))
            self.addToStoryBoardDocument(sortedDocuments[0:self.documentLimit])
            
            self.storyboard['pToN_topics'] = self.sortedTerms(self.scoredTopics['topics'], "position_previous_to_next")
            self.storyboard['nToP_topics'] = self.sortedTerms(self.scoredTopics['topics'], "position_next_to_previous")
            
            # self.storyboard['pToN_actions'] = self.sortedTerms(self.scoredTopics['actions'], "position_previous_to_next")
            # self.storyboard['nToP_actions'] = self.sortedTerms(self.scoredTopics['actions'], "position_next_to_previous")
            
            # self.storyboard['pToN_positives'] = self.sortedTerms(self.scoredTopics['positives'], "position_previous_to_next")
            # self.storyboard['nToP_positives'] = self.sortedTerms(self.scoredTopics['positives'], "position_next_to_previous")
            
            # self.storyboard['pToN_negative'] = self.sortedTerms(self.scoredTopics['negative'], "position_previous_to_next")
            # self.storyboard['nToP_negative'] = self.sortedTerms(self.scoredTopics['negative'], "position_next_to_previous")
            
        if self.datedCount:
            self.storyboard['linegraph'] = self.datedCount
        return
    
    def scoreTerms(self, document, date, fieldKey):
        documentTopics = documentItem[fieldKey].keys()
        if not len(documentTopics):
            return 0
        if fieldKey not in self.scoredTopics.keys():
            self.scoredTopics[fieldKey] = {}
        
        for key in documentItem[fieldKey].keys():
            if key not in self.scoredTopics[fieldKey].keys():
                self.scoredTopics[fieldKey][key] = {
                    "key": key,
                    "pure_word": documentItem['topics']["pure_word"],
                    "description": documentItem['topics']["description"],
                    "position_previous_to_next": 0,
                    "position_next_to_previous": 0,
                    "count": 0
                }
            self.scoredTopics[fieldKey][key]["position_previous_to_next"] += self.getPositionPreviousToNextScore(date)
            self.scoredTopics[fieldKey][key]["position_next_to_previous"] += self.getPositionNextToPreviousScore(date)
            self.scoredTopics[fieldKey][key]["count"] += 1
        return
    
    def addToStoryBoardDocument(self, scoredDocuments):
        self.storyboard['documents'] = []
        for document in scoredDocuments:
            self.storyboard['documents'].append({
                "url": document["url"],
                "title": document["title"],
                "description": document["description"],
                "score": document["score"],
                "date": document["date_key"]
            })
        return
            
    def getDocumentTopicScore(self, documentItem):
        shouldMatched = len(self.topics)
        documentTopics = documentItem['topics'].keys()
        if not len(documentTopics) or not shouldMatched:
            return 0
        
        totalMatched = 0
        score = 0
        for topic in self.topics:
            if topic in documentTopics:
                totalMatched += 1
                score += (documentItem['topics'][topic]['position_weight_forward'] + documentItem['topics'][topic]['position_weight_backward']) / 2
                
        if shouldMatched != totalMatched:
            return 0
        return score / shouldMatched
        
    def load(self):
        if not self.topics or not len(self.topics):
            return
        for key in self.topics:
            self.data = self.rcAnalysis.getRcFileContent(key)
            if self.data:
                break
            
        if self.data:
            self.loadDocuments()
            
        return
    
    def getFormattedMonthOrDay(self, number):
        if int(number) < 10:
            return '0' + number
        return number
    
    def sort(self, items, attribute='score'):
        if not len(items.keys()):
            return []

        sortedTopics = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=True):
            sortedTopics.append(value)

        return sortedTopics
    
    def sortedTerms(self, items, attribute='score', filterAttribute = "count"):
        if not len(items.keys()):
            return []

        sortedItems = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=True):
            if value[filterAttribute] <= self.subTopicDocumentLimit:
                continue
            sortedItems.append(value)

        return sortedItems
    
    def setMinDate(self, date):
        if not self.minDate or (date < self.minDate):
            self.minDate = date
        return 
    
    def setMaxDate(self, date):
        if not self.maxDate or (date > self.maxDate):
            self.maxDate = date
        return 
    
    def strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def daysBetween(self, date1, date2):
        return abs((date1 - date2).days)
    
    def getPositionPreviousToNextScore(self, date):
        totalDays = self.daysBetween(self.maxDate, self.minDate)
        return totalDays - self.daysBetween(self.minDate, date)
    
    def getPositionNextToPreviousScore(self, date):
        totalDays = self.daysBetween(self.maxDate, self.minDate)
        return totalDays - self.daysBetween(self.maxDate, date)
    
    
