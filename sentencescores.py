from math import log
import nltk, operator, re, numpy
from collections import Counter
from nltk.stem.porter import *
from nltk import word_tokenize
from itertools import chain
from sets import Set
from math import sqrt
from networkx import pagerank_numpy, from_numpy_matrix
import operator

"""
    LexRank: Graph-based Centrality as Salience in Text Summarization
    Source: http://tangra.si.umich.edu/~radev/lexrank/lexrank.pdf
"""

class SentenceScores(object):
	def __init__(self):
		self.sentence_score = []
		self.word_score = {}
		self.no_of_sentences = 0
		self.remove_non_alphanumerics = re.compile("[^a-zA-Z0-9-_\s]")
		self.total_no_of_words = 0
		self.word_frequency_count = {}
		self.word_sentence_frequency = {}
		self.stemmer = PorterStemmer()
		self.sentence_tf_scores = []
		self.idf_word_scores = {}
		self.stopwordslist = []

	def get_words(self, sentences):
		words = []

		for sentence in sentences:
			clean_sentence = self.remove_non_alphanumerics.sub('', sentence.lower())
			if len(clean_sentence) > 0:
				words.append([self.stemmer.stem(word) for word in word_tokenize(clean_sentence) if word not in self.stopwordslist])
		
		return words

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


	def calculate_tf_scores(self, sentences):
		words = self.get_words(sentences)
		word_count_map = map(Counter, words)

		tf_sentence_score = []
		for word_list in word_count_map:
			if len(word_list) > 0 :
				sentence_tf_map = {}
				max_frequency = max(word_list.values())

				for word in word_list.keys():
					frequency = word_list[word]
					sentence_tf_map[word] = (frequency*1.0)/max_frequency

				tf_sentence_score.append(sentence_tf_map)

		self.sentence_tf_scores = tf_sentence_score

	def calculate_idf_scores(self, sentences):
		no_of_sentences = len(sentences)
		words = self.get_words(sentences)

		docs_words_iterable = chain.from_iterable(words)
		docs_words_list = list(docs_words_iterable)
		word_counts_counter = map(Counter, [docs_words_list]) # Counter requires list of lists
		word_counts = word_counts_counter[0]

		idf_score = {}
		for word in Set(docs_words_list):
			idf_score[word] = (no_of_sentences*1.0) / word_counts[word]

		self.idf_word_scores = idf_score

	def calculate_idf_cosine(self, sentence1_words, sentence2_words, sentence1_tf, sentence2_tf):
		set_of_common_words = sentence1_words & sentence2_words
		common_words = list(set_of_common_words)

		sentence1_denom = sum(pow(sentence1_tf[word]*self.idf_word_scores[word], 2) for word in sentence1_words)
		sentence2_denom = sum(pow(sentence2_tf[word]*self.idf_word_scores[word], 2) for word in sentence2_words)

		numerator = 0.0
		denominator = 1.0
		if sentence2_denom > 0 and sentence1_denom > 0:
			numerator = sum(map((lambda word: sentence1_tf[word]*sentence2_tf[word]*pow(self.idf_word_scores[word], 2)) , common_words))
			denominator = sqrt(sentence1_denom) * sqrt(sentence2_denom)

		return numerator/denominator

	def create_similarity_matrix(self, sentences):
		size = len(sentences)
		cosine_matrix = numpy.zeros((size, size))
		degree_vector = numpy.zeros((size, ))
		sentences_with_tf = zip(sentences, self.sentence_tf_scores)

		for row, (sentence1, sentence1_tf) in enumerate(sentences_with_tf):
			sentence1_words = self.get_words([sentence1])
			for col, (sentence2, sentence2_tf) in enumerate(sentences_with_tf):
				if row == col:
					cosine_matrix[row][col] = 1
					break
				sentence2_words = self.get_words([sentence2])
				cosine_matrix[row][col] = self.calculate_idf_cosine(frozenset(sentence1_words[0]), frozenset(sentence2_words[0]), sentence1_tf, sentence2_tf)

		row_sums = cosine_matrix.sum(axis=1)
		stochastic_cosine_matrix = cosine_matrix / row_sums[:, numpy.newaxis]

		return stochastic_cosine_matrix

	def lexrank_power_iteration(self, stochastic_cosine_matrix, no_of_sentences, error_threshold):
		graph = from_numpy_matrix(stochastic_cosine_matrix)
		return pagerank_numpy(graph)



	def get_summary_lines(self, sentences):
		with open("/home/sesha/Subjects/Summer2K15/UN/summary-ly/stopwords-english.txt") as stopwordsfile:
			self.stopwordslist.append(stopwordsfile.readlines())

		self.calculate_tf_scores(sentences)
		self.calculate_idf_scores(sentences)
		stochastic_cosine_matrix = self.create_similarity_matrix(sentences)
		sentences_eigen_values = self.lexrank_power_iteration(stochastic_cosine_matrix, len(sentences), 0.1)
		sentence_by_importance = sorted(sentences_eigen_values.items() ,key=operator.itemgetter(1))
		# return [sentences.index(sentence_score) for sentence_score in sentences_eigen_values]# if score_for_sentence > 0.12]
		sentence_by_importance.reverse()
		return sentence_by_importance
