import tika, sys
from tika import parser
from sentencescores import SentenceScores

def main(file_name):
	score_sentences = SentenceScores()

	parsed = parser.from_file(file_name)
	content = parsed["content"]
	sentences = content.split(".")
	
	lines = score_sentences.get_summary_lines(sentences)
	print lines


if __name__ == "__main__":
   sys.exit(main(sys.argv[1]))