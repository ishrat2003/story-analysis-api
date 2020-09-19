import re
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import utility

class LCStory():
    
    def __init__(self, filter = 30):
        self.stopWords = utility.Utility.getStopWords()
        self.punctuationTypes = ['.', '?', '!']
        self.stemmer = PorterStemmer()
        self.__loadGroups()
        self.setOccuranceContributingFactor(1)
        self.setPositionContributingFactor(1)
        self.filter = filter
        return
    
    def setPositionContributingFactor(self, contributingFactor):
        self.positionContributingFactor = contributingFactor
        return

    def setOccuranceContributingFactor(self, contributingFactor):
        self.occuranceContributingFactor = contributingFactor
        return
    
    def getConcepts(self, text, highestNgrams):
        validNgrams  = []
        self.__reset(text)
        self.setProspectiveProperNouns()
        self.setSentences()
        return self.data
    
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
            
        self.data['sentences'] = sentences
        self.data['after_filter_total_words'] = len(self.data['wordsInfo'].keys())
        return
    
    def _addWordInfo(self, word, type, currentPositionValue):
        if type not in self.allowedPOSTypes:
            return

        if word in self.stopWords:
            return
        
        wordLower = word.lower()
        wordKey = self.stemmer.stem(wordLower)
        localWordInfo = {}
        localWordInfo['type'] = type
        localWordInfo['pure_word'] = word
        localWordInfo['stemmed_word'] = wordKey
        
        if localWordInfo['stemmed_word'] in self.data['wordsInfo'].keys():
            return
        
        isProperNoun = False
        if (type in ['NNP', 'NNPS']):
            if (wordLower not in self.properNouns.keys()):
                return 
            localWordInfo['pure_word'] = self.properNouns[wordLower]
            isProperNoun = True

        localWordInfo['index'] = len(self.data['wordsInfo'])
        localWordInfo['first_position'] = currentPositionValue
        localWordInfo['position_weight'] = (currentPositionValue / self.data['total_sentences']) * 100
        localWordInfo['count'] = self.__getCount(localWordInfo['stemmed_word'])
        localWordInfo['occurance_weight'] = (localWordInfo['count'] / self.data['total_words']) * 100
        localWordInfo['score'] = (self.positionContributingFactor * localWordInfo['position_weight']
            + self.occuranceContributingFactor * localWordInfo['occurance_weight']) / 2
        
        if localWordInfo['score'] < self.filter:
            return
        
        if isProperNoun:
            self.data['proper_nouns'].append(localWordInfo['pure_word'])
        
        self.data['wordsInfo'][wordKey] = localWordInfo
        print(self.data['wordsInfo'][wordKey])
        return
    
    def __getWords(self, text):
        words = word_tokenize(text)
        return pos_tag(words)
    
    def __getRawSentences(self, text):
        text = re.sub(r'([0-9]+)\.([0-9]+)', r'\1##\2', text)
        text = re.sub(r'\.', r'#END#', text)
        text = re.sub(r'([0-9]+)##([0-9]+)', r'\1.\2', text)
        return re.split("\n|#END#|!|\?", text)
    
    def __getCount(self, value):
        list = re.findall(value, self.text, flags=re.IGNORECASE)
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
            'proper_nouns': [],
            'sentences': [],
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
        self.wordPosGroups['adjective'] = ['JJ', 'JJR', 'JJS']
        self.wordPosGroups['adverb'] = ['RB', 'RBR', 'RBS']
        self.wordPosGroups['verb'] = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        
        self.allowedPOSTypes = []
        posGroupKeys = self.wordPosGroups.keys()
        if not posGroupKeys:
            return
        
        for key in posGroupKeys:
            self.allowedPOSTypes = list(set(self.allowedPOSTypes + self.wordPosGroups[key]))

        return
