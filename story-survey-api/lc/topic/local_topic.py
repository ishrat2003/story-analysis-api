import re
from .cwr import CWR

class LocalTopic(CWR):
    
    def __init__(self):
        super().__init__()
        return
    
    def getNgrams(self, text, highestNgrams):
        validNgrams  = []
        return text
    
    def get(self, text, allowedScoreRatio = 0.1):
        self._reset()
        self.loadSentences(text)
        self.loadScore()
        self.setMaxAllowedRadius(allowedScoreRatio)
        self.sort()
        self.properNouns = list(set(self.getProperNouns()))
        
        for word in self.wordsInfo.keys():
            self._addPriorityWords(self.wordsInfo[word])

        self.filteredWordsByType['proper_noun'] = self.properNouns
        return [self.filteredWordsByType, self.getTopicsToDisplay()]
    
    def getTopicsToDisplay(self, limit = 5):
        wordsToDisplay = []
        for type in ['noun', 'adjective', 'adverb', 'negative', 'adverb', 'verb', 'positive']:
            wordsByType = self.filteredWordsByType[type][0:limit]
            for word in wordsByType:
                word['color_group'] = type
                word['name'] = self._getDisplayName(word)
                wordsToDisplay.append(word)
                
        return wordsToDisplay
    
    def _addPriorityWords(self, word):
        if word['score'] < self.maxAllowedScore:
            return

        for typeName in self.wordPosGroups.keys():
            if word['type'] in self.wordPosGroups[typeName]:
                self.filteredWordsByType[typeName].append(word)

        if word['stemmed_word'] in self.positiveWords:
            self.filteredWordsByType['positive'].append(word)
            if self.filteredWordsByType[typeName]:
                self.filteredWordsByType[typeName].pop()

        if word['stemmed_word'] in self.negativeWords:
            self.filteredWordsByType['negative'].append(word)
            if self.filteredWordsByType[typeName]:
                self.filteredWordsByType[typeName].pop()
        return
    
    def _getDisplayName(self, word):
        if self.properNouns and word['color_group']  == 'noun':
            for properName in self.properNouns:
                if word['pure_word']in properName:
                    return properName;
                
        return word['pure_word'][0].upper() + word['pure_word'][1:]
    
    def _reset(self):
        super()._reset()
        self.filteredWordsByType = {}
        for type in ['proper_noun', 'noun', 'adjective', 'adverb', 'verb', 'positive', 'negative']:
            self.filteredWordsByType[type] = []
        return
    
    
    def __getCount(self, value, text):
        list = re.findall(value, value, text)
        return len(list)
