import datetime, operator

class Base:
    
    def __init__(self, params):
        self.dataDates = {
            'max': None,
            'min': None
        }
        self.params = params
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
        if (('start' not in self.params.keys()) 
            or not self.params['start'] 
            or self.isGreaterThanMin(self.params['start'])):
            self.dataDates['start'] = self.dataDates['min']
        else:
            self.dataDates['start'] = self.params['start']
        return
    
    def setEnd(self):
        if (('end' not in self.params.keys()) 
            or not self.params['end'] 
            or self.isLessThanMax(self.params['end'])):
            self.dataDates['end'] = self.dataDates['max']
        else:
            self.dataDates['end'] = self.params['end']
        return
    
    def isGreaterThanMin(self, date):
        date = self.strToDate(date)
        minDate = self.strToDate(self.dataDates['min'])
        return date > minDate
    
    def isLessThanMax(self, date):
        date = self.strToDate(date)
        maxDate = self.strToDate(self.dataDates['max'])
        return date < maxDate
    
    def strToDate(self, date):
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    
    def getFormattedMonthOrDay(self, number):
        if int(number) < 10:
            return '0' + str(number)
        return number

    def getMaxMin(self, items):
        listKeys = list(map(int, items))
        listKeys = sorted(listKeys)
        totalItems = len(listKeys)
        min = listKeys[0]
        max = listKeys[totalItems - 1]
        return str(min), str(max)
    
    def sort(self, items, attribute='total_block_count_in_range', reverse=True):
        if not len(items.keys()):
            return []

        sortedTopics = []
        contributors = items.values()
        
        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=reverse):
            sortedTopics.append(value)

        return sortedTopics
    
    def getSplited(self, date):
        return [int(x) for x in date.split("-")]
    
    def unformattedStrToDate(self, date):
        year, month, day = self.getSplited(date)
        return self.strToDate(str(year) + '-' + str(self.getFormattedMonthOrDay(month)) + '-' + str(self.getFormattedMonthOrDay(day)))
        
