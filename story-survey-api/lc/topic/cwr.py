
from nltk.stem.porter import PorterStemmer
import utility
from .word import Word

class CWR(Word):

	def __init__(self):
		super().__init__()
		self.setOccuranceContributingFactor(0)
		self.setPositionContributingFactor(1)
		self.setProperNounContributingFactor(0)
		self.positiveWords = utility.Utility.getPositiveWords()
		self.negativeWords = utility.Utility.getNegativeWords()
		return


	def setPositionContributingFactor(self, contributingFactor):
		self.positionContributingFactor = contributingFactor
		return


	def setOccuranceContributingFactor(self, contributingFactor):
		self.occuranceContributingFactor = contributingFactor
		return
   
    
	def setProperNounContributingFactor(self, contributingFactor):
		self.properNounContributingFactor = contributingFactor
		return


	def setMaxAllowedRadius(self, allowedScoreRatio = 0.9):
		self.maxAllowedScore = self.maxScore * allowedScoreRatio
		return


	def getProperNouns(self):
		return self.properNouns


	def loadScore(self, allowedScoreRatio = 0.9):
		totalWords = len(self.wordsInfo.keys())

		if totalWords == 0:
			return

		currentTheta = 0
		unitTheta = 360 / totalWords

		for word in self.wordsInfo.keys():
			self.wordsInfo[word]['score'] = self.__getScore(self.wordsInfo[word])
			self.wordsInfo[word]['theta'] = currentTheta
			currentTheta += unitTheta

		return 


	def __getScore(self, word):
		score = 0
		score += word['count'] * self.occuranceContributingFactor
		if 'proper_noun' in word.keys():
			score += word['proper_noun'] * self.properNounContributingFactor
		for position in word['positions']:
			score += (self.maxPosition - position) * self.positionContributingFactor

		if self.maxScore < score:
			self.maxScore = score
		return score


	def addToProperNoun(self, mainWord):
		if self.lastNounProperNoun:
			lastIndex = len(self.properNouns) - 1
			self.properNouns[lastIndex] = self.properNouns[lastIndex] + ' ' + mainWord
		elif mainWord not in self.properNouns:	
			self.properNouns.append(mainWord)

		return


	def _addWordInfo(self, word, type):
		if type not in ['NNP', 'NNPS']:
			self.lastNounProperNoun = False

		if not word or (type not in self.allowedPOSTypes):
			return None

		if word in self.stopWords:
			return None

		wordKey = super()._addWordInfo(word, type)
		keys = self.wordsInfo[wordKey].keys()
		if 'positions' not in keys:
			self.wordsInfo[wordKey]['positions'] = []

		if 'proper_noun' not in keys:
			self.wordsInfo[wordKey]['proper_noun'] = 0

		self.wordsInfo[wordKey]['positions'].append(self.maxPosition)
		if type in ['NNP', 'NNPS']:
			self.wordsInfo[wordKey]['proper_noun'] += 1
			self.addToProperNoun(word)
			self.lastNounProperNoun = True
		else:
			self.lastNounProperNoun = False

		self.maxPosition += 1
		return wordKey


	def _reset(self):
		super()._reset()
		self.maxPosition = 0
		self.properNouns = []
		self.lastNounProperNoun = False
		self.maxScore = 0
		self.macAllowedRadius = 0
		return

