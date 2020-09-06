import re
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import utility
import operator

class Word:

    def __init__(self):
        super().__init__()
        self.stopWords = utility.Utility.getStopWords()
        self.punctuationTypes = ['.', '?', '!']
        self.stemmer = PorterStemmer()
        self.minWordSize = 2
        self.__loadGroups()
        return

    def loadSentences(self, text):
        self._reset()
        text = self.__clean(text)
        words = self.__getWords(text)
        if not len(words):
            return

        for word in words:
            (word, type) = word
            word = self.__cleanWord(word)

            if type in self.punctuationTypes:
                if len(self.currentSentence) > 1:
                    # If more than one word than add as sentence
                    self.sentences.append(self.currentSentence)
                self.currentSentence = []

            if (len(word) < self.minWordSize) or (word in self.stopWords):
                continue

            wordKey = self._addWordInfo(word, type)
            if wordKey and (wordKey not in self.currentSentence):
                self.currentSentence.append(wordKey)

            # Processing last sentence
            if len(self.currentSentence) > 1:
                # If more than one word than add as sentence
                self.sentences.append(self.currentSentence)

        return

    def sort(self, attribute='score'):
        if not len(self.wordsInfo):
            return

        sortedWords = {}
        contributors = self.wordsInfo.values()

        for value in sorted(contributors, key=operator.itemgetter(attribute), reverse=True):
            sortedWords[value['stemmed_word']] = value

        self.wordsInfo = sortedWords
        return


    def _addWordInfo(self, word, type):
        if not word or (type not in self.allowedPOSTypes):
            return None

        if word in self.stopWords:
            return None

        localWordInfo = {}
        localWordInfo['pure_word'] = word
        wordKey = self.stemmer.stem(word.lower())
        localWordInfo['stemmed_word'] = wordKey
        localWordInfo['type'] = type

        if localWordInfo['stemmed_word'] in self.wordsInfo.keys():
            self.wordsInfo[wordKey]['count'] += 1
            if self.maxCount < self.wordsInfo[wordKey]['count']:
                self.maxCount = self.wordsInfo[wordKey]['count']
            return wordKey

        localWordInfo['count'] = 1
        localWordInfo['index'] = len(self.wordsInfo)
        self.wordsInfo[wordKey] = localWordInfo

        return wordKey
    
    
    def _reset(self):
        self.maxCount = 0
        self.wordsInfo = {}
        self.sentences = []
        self.currentSentence = []
        return
    
    
    def __getWords(self, text):
        words = word_tokenize(text)
        return pos_tag(words)
    
    
    def __clean(self, text):
        text = re.sub('<.+?>', '. ', text)
        text = re.sub('&.+?;', '', text)
        text = re.sub('[\']{1}', '', text)
        text = re.sub('[^a-zA-Z0-9\s_\-\?:;\.,!\(\)\"]+', ' ', text)
        text = re.sub('\s+', ' ', text)
        text = re.sub('(\.\s*)+', '. ', text)
        return text


    def __cleanWord(self, word):
    	return re.sub('[^a-zA-Z0-9]+', '', word)

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
