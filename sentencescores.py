from math import log
import nltk, operator, re
from nltk.corpus import stopwords

"""
    LexRank: Graph-based Centrality as Salience in Text Summarization
    Source: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
"""

class SentenceScores(object):
	def __init__(self):
		self.sentence_score = []
		self.word_score = {}
		self.no_of_sentences = 0
		self.stopwordlist = stopwords.words('english')
		self.remove_non_alphanumerics = re.compile("[^a-zA-Z0-9-_\s]")
		self.total_no_of_words = 0
		self.word_frequency_count = {}
		self.word_sentence_frequency = {}

	def get_words(self, sentence):
		clean_sentence = self.remove_non_alphanumerics.sub('', sentence.lower())
		return [word for word in clean_sentence.split() if word not in self.stopwordlist]

	def calculate_tfidf(self, word):
		tf = ((self.word_frequency_count[word] * 1.0) / self.total_no_of_words)
		word_sentence_exist_count = len(self.word_sentence_frequency[word])
		idf = log((self.no_of_sentences * 1.0)/word_sentence_exist_count)

		return (tf * idf)

	# one single array of all sentences
	def map_word_to_segment(self, sentences):
		sentence_count = 0
		self.no_of_sentences = len(sentences)
		for sentence in sentences:
			words = self.get_words(sentence)
			sentence_count += 1

			self.total_no_of_words += len(sentence.split())
			for word in words:
				if word not in self.word_frequency_count:
					self.word_frequency_count[word] = 0
				self.word_frequency_count[word] += 1
		
				if word not in self.word_sentence_frequency:
					self.word_sentence_frequency[word] = set()
				self.word_sentence_frequency[word].add(sentence_count)

	def score_words(self):
		for word in self.word_frequency_count:
			self.word_score[word] = self.calculate_tfidf(word)

	def score_sentences(self, sentences):
		for sentence in sentences:
			words = self.get_words(sentence)
			if len(words) > 0:
				self.sentence_score.append(reduce((lambda a, b: a+b), [self.word_score[word] for word in words]))


	def get_summary_lines(self, sentences):
		self.map_word_to_segment(sentences)
		self.score_words()
		self.score_sentences(sentences)
		score_sort_array = list(self.sentence_score)
		score_sort_array.sort(reverse=True)
		return [self.sentence_score.index(score_for_sentence) for score_for_sentence in score_sort_array if score_for_sentence > 0.12]
