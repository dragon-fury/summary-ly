import tika, sys, re
from tika import parser
from sentencescores import SentenceScores
import operator

def clean_sentence(sentence):
	replace_linefeed = re.compile("\n")
	temp = replace_linefeed.sub(" ", sentence)
	temp.strip()
	return temp + "\n"

def main(file_name):
	fi = open("sentences.txt", "w+")
	fi_summary = open("summary.txt", "w+")
	fi_cool = open("wtv.txt", "w+")
	score_sentences = SentenceScores()

	parsed = parser.from_file(file_name)
	print parsed["metadata"]
	content = parsed["content"]
	content = content.strip()
	fi_cool.write(content.encode("utf-8"))
	sentences = content.split(". ")
	sentences = map(clean_sentence, sentences)
	
	lines = score_sentences.get_summary_lines(sentences)
	max_len = len(lines) / 3
	needed_lines = lines[0:max_len]
	sorted_lines = sorted(needed_lines, key=lambda x: x[0])

	for line_num, score in sorted_lines:
		fi_summary.write((str(line_num+1)+", "+sentences[line_num]).encode("utf-8"))

	for sentence in sentences:
		fi.write(sentence.encode("utf-8"))

	fi.close()
	fi_summary.close()


if __name__ == "__main__":
   sys.exit(main(sys.argv[1]))