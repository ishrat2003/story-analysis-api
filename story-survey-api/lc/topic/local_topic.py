from .cwr import CWR

class LocalTopic(CWR):
    
    def __init__(self):
        super().__init__()
        return
    
    def get(self, text, allowedScoreRatio = 0.5):
        self._reset()
        self.loadSentences(text)
        self.loadScore()
        self.setMaxAllowedRadius(allowedScoreRatio)
        
        for word in self.wordsInfo.keys():
            self._addPriorityWords(self.wordsInfo[word])
        
        topics = self.filteredWordsByType
        topics['joint_proper_noun'] = self.getProperNouns()
         
        return topics
    
    
    def _addPriorityWords(self, word):
        if word['score'] < self.maxAllowedScore:
            return

        displayName = self._getDisplayName(word)
        for typeName in self.wordPosGroups.keys():
            if word['type'] in self.wordPosGroups[typeName]:
                self.filteredWordsByType[typeName].append(displayName)

        if word['stemmed_word'] in self.positiveWords:
            self.filteredWordsByType['positive'].append(displayName)

        if word['stemmed_word'] in self.negativeWords:
            self.filteredWordsByType['negative'].append(displayName)
        
        return
    
    def _getDisplayName(self, word):
        return word['pure_word'] + ' - ' + str(word['score'])
    
    def _reset(self):
        super()._reset()
        self.filteredWordsByType = {}
        for type in ['joint_proper_noun', 'proper_noun', 'noun', 'adjective', 'adverb', 'verb', 'positive', 'negative']:
            self.filteredWordsByType[type] = []
        return