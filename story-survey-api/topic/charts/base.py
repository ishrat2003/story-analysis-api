import datetime, operator

class Base:
    
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
    
    def sort(self, items, attribute='total_block_count'):
        if not len(items.keys()):
            return []

        sortedTopics = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=True):
            sortedTopics.append(value)

        return sortedTopics