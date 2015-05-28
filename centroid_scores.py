from math import log
import nltk, operator
from nltk.corpus import stopwords

class CentroidScores(object):
	def __init__(self):
		self.word_freq_score = {}
		self.sentence_score = []
		self.word_score = {}
		self.all_sentences = []
		self.no_of_segments = 0
		self.stopwordlist = stopwords.words('english')
		self.remove_non_alphanumerics = re.compile("[^a-zA-Z0-9-_\s]")
		self.corpora = set()
		self.word_segment_mapping = {}


	# word_para_exist_count
	# get (Sentence, para, line) tuple
	# 
	def calculate_idf(word):
		word_para_exist_count = len(self.word_segment_mapping[word])
		return log(self.no_of_segments/word_para_exist_count)

	# text_by_para is input sentences in array of arrays for paras
	def map_word_to_segment(text_by_para):
		self.no_of_segments = len(text_by_para)
		for sentence_tuples in text_by_para:
			for sentence_tuple in sentence_tuples:
				words = set(get_words(sentence_tuple[0]))
				# self.corpora.update(words)
				for word in words:
					if word not in self.word_segment_mapping:
						self.word_segment_mapping[word] = set()
					self.word_segment_mapping[word].add(sentence_tuple[1])

	def score_words():
		for word in self.word_segment_mapping:
			self.word_score[word] = calculate_idf(word)


	def get_words(sentence):
		clean_sentence = self.remove_non_alphanumerics.sub('', sentence.lower())
		content = [word for word in clean_sentence.split() if word not in self.stopwordlist]

	def score_sentences():
		for sentence_tuples in text_by_para:
			for sentence_tuple in sentence_tuples:
				words = get_words(sentence_tuple[0])

