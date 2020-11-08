import re, operator, math
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import utility

class LCStory():
    
    def __init__(self, filter = 0):
        self.stopWords = utility.Utility.getStopWords()
        self.punctuationTypes = ['.', '?', '!']
        self.stemmer = PorterStemmer()
        self.__loadGroups()
        self.setOccuranceContributingFactor(1)
        self.setPositionContributingFactor(1)
        self.filter = filter
        self.positiveWords = utility.Utility.getPositiveWords()
        self.negativeWords = utility.Utility.getNegativeWords()
        self.splits = 5
        self.minCharLength = 1
        return
    
    def setPositionContributingFactor(self, contributingFactor):
        self.positionContributingFactor = contributingFactor
        return

    def setOccuranceContributingFactor(self, contributingFactor):
        self.occuranceContributingFactor = contributingFactor
        return
    
    def getConcepts(self, text):
        self.__reset(text)
        self.setProspectiveProperNouns()
        self.setSentences()
        # pwfWords = self.sort('position_weight_forward')
        # self.data['sorted_words']['position_weight_forward'] = self.getDisplayByGroup(pwfWords, 'position_weight_forward', 90)
        
        # pwbWords = self.sort('position_weight_backward')
        # self.data['sorted_words']['position_weight_backward'] = self.getDisplayByGroup(pwbWords, 'position_weight_backward', 90)
        
        # words = self.sort('occurance_weight')
        # self.data['sorted_words']['occurance_weight'] = self.getDisplayByGroup(words, 'occurance_weight', 0)
        
        # words = self.sort('count')
        # self.data['sorted_words']['count'] = self.getDisplayByGroup(words, 'count', 2)
        
        # words = self.sort('first_block')
        # self.data['sorted_words']['first_block'] = self.getDisplayByGroup(words, 'first_block', 0)

        self.loadAnalyzedWords()
        return self.data
    
    def loadAnalyzedWords(self):
        pwfWords = self.sort('position_weight_forward')
        pwbWords = self.sort('position_weight_backward')
        
        if not len(pwfWords) or not len(pwbWords):
            return
        
        analyzedKeys = self.data['story_words_keys']
        analyzedKeys = self.getKeys(pwfWords, analyzedKeys, 'position_weight_forward')
        print(analyzedKeys)
        
        for wordKey in pwfWords.keys():
            word = pwfWords[wordKey]
            if ((len(word['blocks']) >= math.floor(self.splits / 2)) and (wordKey not in analyzedKeys)):
                analyzedKeys.append(wordKey)
        
        analyzedKeys = self.getKeys(pwbWords, analyzedKeys, 'position_weight_backward')
        self.data['story_words_keys'] = analyzedKeys
        
        for key in analyzedKeys:
            word = self.data['wordsInfo'][key]
            self.data['story_words'].append(word)
            if word['type'] in ['NNP', 'NNPS']:
                display = word['pure_word'][0].upper() + word['pure_word'][1:]
                if display not in self.data['topic_words']:
                    self.data['topic_words'].append(display)
                    
        self.data['total_topic_words'] = len(self.data['topic_words'])
        self.data['total_story_words'] = len(self.data['story_words'])
        return
    
    def getKeys(self, words, wordKeys, key = 'position_weight_forward', minItems = 10, minWeights = 2):
        totalWeightsConsidered = []
        for wordKey in words.keys():
            if (len(totalWeightsConsidered) > minWeights) and (len(wordKeys) > minItems):
                break
            
            if wordKey not in wordKeys:
                wordKeys.append(wordKey)
                if words[wordKey][key] not in totalWeightsConsidered:
                    totalWeightsConsidered.append(words[wordKey][key])
                
        return wordKeys
    
    def setProspectiveProperNouns(self):
        if len(self.properNouns.keys()):
            return
        
        items = re.finditer('([A-Z][a-z0-9\-]+\s*)+', self.text)
        if not items:
            return
        
        for item in items:
            words = item.group(0).split(' ')
            properNoun = []
            for word in words:
                word = word.strip()
                lowerWord = word.lower()
                if lowerWord in self.stopWords:
                    continue
                properNoun.append(word)
            if properNoun:
                indexNoun = properNoun[-1].lower()
                if indexNoun in  self.properNouns.keys():
                  continue  
                self.properNouns[indexNoun] = ' '.join(properNoun)
        return
    
    def setSentences(self):
        if len(self.data['sentences']):
            return
        
        sentences = self.__getRawSentences(self.text)
        self.data['total_sentences'] = len(sentences)
        self.data['threshold'] = math.ceil(self.data['total_sentences'] / self.splits)
        currentPositionValue = self.data['total_sentences']
        self.data['total_words'] += self.__getTotalWords()
        
        for sentence in sentences:
            if not sentence: 
                continue
            
            words = self.__getWords(sentence)
            
            for word in words:
                (word, type) = word
                self._addWordInfo(word, type, currentPositionValue)
            
            
            currentPositionValue -= 1
            #self.data['sentences_with_type'] += ' .'
            
        self.data['sentences'] = sentences
        self.data['after_filter_total_words'] = len(self.data['wordsInfo'].keys())
        return
    
    
    def sort(self, attribute='score'):
        if not len(self.data['wordsInfo'].keys()):
            return

        sortedWords = {}
        contributors = self.data['wordsInfo'].values()

        
        for value in sorted(contributors, key=operator.itemgetter(attribute, 'count'), reverse=True):
            sortedWords[value['stemmed_word']] = value

        return sortedWords
    
    def  getDisplayByGroup(self, words, attribute = 'score', min = 95):
        wordsToDisplay = {}
        for word in words:
            type = words[word]['color_group']
            if type not in wordsToDisplay.keys():
                wordsToDisplay[type] = []
            
            if words[word][attribute] >= min:
                item = words[word]['pure_word'] \
                + '(' + str(words[word][attribute]) + ')' \
                + '(' + ','.join(str(x) for x in words[word]['blocks']) + ')' \
                + '(' + str(words[word]['position_weight_forward']) + ')' \
                + '(' + str(words[word]['position_weight_backward']) + ')' \
                + '(' + str(words[word]['count']) + ')'
                
                wordsToDisplay[type].append(item)
        return wordsToDisplay
    
    def _addWordInfo(self, word, type, currentPositionValue):
        if (type not in self.allowedPOSTypes) or (len(word) <= self.minCharLength):
            # print(word, '    ', type)
            return

        if word in self.stopWords:
            return
        wordLower = word.lower()
        wordKey = self.stemmer.stem(wordLower)
        localWordInfo = {}
        localWordInfo['type'] = type
        localWordInfo['pure_word'] = word
        localWordInfo['stemmed_word'] = wordKey
        
        #self.data['sentences_with_type'] += ' ' + type + '##' + wordKey + ' '
        blockNumber = (currentPositionValue // self.data['threshold'])
        
        if localWordInfo['stemmed_word'] in self.data['wordsInfo'].keys():
            localWordInfo = self.data['wordsInfo'][wordKey]
            localWordInfo['count'] += 1
            localWordInfo['position_weight_backward'] = ((self.data['total_sentences'] - currentPositionValue) / self.data['total_sentences']) * 100
            
            if blockNumber not in localWordInfo['blocks']:
                localWordInfo['blocks'].append(blockNumber)
                
            self.data['wordsInfo'][wordKey] = localWordInfo
            if len(localWordInfo['blocks']) == self.splits:
                if wordKey not in self.data['story_words_keys']:
                    self.data['story_words_keys'].append(wordKey)
            return
        
        
        localWordInfo['blocks'] = [blockNumber]
        localWordInfo['first_block'] = blockNumber
        
        isProperNoun = False
        if (type in ['NNP', 'NNPS']):
            if (wordLower not in self.properNouns.keys()):
                return 
            localWordInfo['pure_word'] = self.properNouns[wordLower]
            isProperNoun = True

        localWordInfo['index'] = len(self.data['wordsInfo'])
        localWordInfo['first_position'] = currentPositionValue
        localWordInfo['position_weight_forward'] = (currentPositionValue / self.data['total_sentences']) * 100
        localWordInfo['position_weight_backward'] = ((self.data['total_sentences'] - currentPositionValue) / self.data['total_sentences']) * 100
        #localWordInfo['count'] = self.__getCount(wordKey)
        localWordInfo['count'] = 1
        localWordInfo['occurance_weight'] = (localWordInfo['count'] / self.data['total_words']) * 100
        localWordInfo['score'] = (self.positionContributingFactor * localWordInfo['position_weight_forward']
            + self.occuranceContributingFactor * localWordInfo['count'])
        
        
        if isProperNoun:
            self.data['proper_nouns'].append(localWordInfo['pure_word'])

        for typeName in self.wordPosGroups.keys():
            if localWordInfo['type'] in self.wordPosGroups[typeName]:
                localWordInfo['color_group'] = typeName
                break
                
        if localWordInfo['stemmed_word'] in self.positiveWords:
            localWordInfo['color_group'] = 'positive'
            localWordInfo['sentiment'] = 'positive'

        if localWordInfo['stemmed_word'] in self.negativeWords:
            localWordInfo['color_group'] = 'negative'
            localWordInfo['sentiment'] = 'negative'
            
        self.data['wordsInfo'][wordKey] = localWordInfo
        # print(self.data['wordsInfo'][wordKey])
        return
    
    def __getWords(self, text):
        words = word_tokenize(text)
        return pos_tag(words)
    
    def __getRawSentences(self, text):
        text = re.sub(r'([0-9]+)\.([0-9]+)', r'\1##\2', text)
        text = re.sub(r'\.', r'#END#', text)
        text = re.sub(r'([0-9]+)##([0-9]+)', r'\1.\2', text)
        text = re.split("\n|#END#|!|\?", text)
        return list(filter(lambda sentence: len(sentence) > 0, text))
    
    def __getCount(self, value):
        list = re.findall('\s' + value, self.text, flags=re.IGNORECASE)
        return len(list)
    
    def __getTotalWords(self):
        list = re.findall("(\S+)", self.text)
        # Return length of resulting list.
        return len(list)
     
    def __reset(self, text):
        self.text = text
        self.properNouns = {}
        self.data = {
            'total_words': 0,
            'after_filter_total_words': 0,
            'total_sentences': 0,
            'threshold': 0,
            'total_topic_words': 0,
            'topic_words': [],
            'total_story_words': 0,
            'story_words': [],
            'story_words_keys': [],
            'proper_nouns': [],
            'sorted_words': {},
            'sentences': '',
            #'sentences_with_type': '',
            'wordsInfo': {}
        }
        return
    
    '''
    CC coordinating conjunction
    CD cardinal digit
    DT determiner
    EX existential there (like: “there is” … think of it like “there exists”)
    FW foreign word
    IN preposition/subordinating conjunction
    JJ adjective ‘big’
    JJR adjective, comparative ‘bigger’
    JJS adjective, superlative ‘biggest’
    LS list marker 1)
    MD modal could, will
    NN noun, singular ‘desk’
    NNS noun plural ‘desks’
    NNP proper noun, singular ‘Harrison’
    NNPS proper noun, plural ‘Americans’
    PDT predeterminer ‘all the kids’
    POS possessive ending parent’s
    PRP personal pronoun I, he, she
    PRP$ possessive pronoun my, his, hers
    RB adverb very, silently,
    RBR adverb, comparative better
    RBS adverb, superlative best
    RP particle give up
    TO, to go ‘to’ the store.
    UH interjection, errrrrrrrm
    VB verb, base form take
    VBD verb, past tense took
    VBG verb, gerund/present participle taking
    VBN verb, past participle taken
    VBP verb, sing. present, non-3d take
    VBZ verb, 3rd person sing. present takes
    WDT wh-determiner which
    WP wh-pronoun who, what
    WP$ possessive wh-pronoun whose
    WRB wh-abverb where, when
    '''
    def __loadGroups(self):
        self.wordPosGroups = {}
        self.wordPosGroups['noun'] = ['NN', 'NNS', 'NNP', 'NNPS']
        #self.wordPosGroups['adjective'] = ['JJ', 'JJR', 'JJS']
        #self.wordPosGroups['adverb'] = ['RB', 'RBR', 'RBS']
        self.wordPosGroups['verb'] = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        #self.wordPosGroups['combined'] = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']
        # self.wordPosGroups['other'] = ['IN', 'TO']
        
        self.allowedPOSTypes = []
        posGroupKeys = self.wordPosGroups.keys()
        if not posGroupKeys:
            return
        
        for key in posGroupKeys:
            self.allowedPOSTypes = list(set(self.allowedPOSTypes + self.wordPosGroups[key]))

        return
