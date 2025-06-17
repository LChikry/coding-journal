import math
import re
import numpy as np
from functools import reduce

text = '''Humpty Dumpty sat on a wall
Humpty Dumpty had a great fall
all the king's horses and all the king's men
couldn't put Humpty together again'''

def get_manh_dist(a, b):
	return sum(abs(x - y) for x, y in zip(a, b))

def main(text):
	# preprocessing text
	lines = re.sub(r"'s\b|[^\w\s]", "", text).lower().split('\n')
	corpus = list(map(lambda x: x.split(), lines))
	vocabulary = sorted(set(word for doc in corpus for word in doc))
	
	# calculating IDF
	idf = dict()
	for word in vocabulary:
		idf[word] = sum(1 for doc in corpus if word in doc)
	num_docs = len(corpus)
	idf = {word: math.log10(num_docs / (1+df)) for word, df in idf.items()}

	# calculating IF-IDF for each doc
	vocabulary_index = {word: i for i, word in enumerate(vocabulary)}
	vectored_corpus = []
	for doc in corpus:
		tf = [0] * len(vocabulary)
		doc_len = len(doc)
		for word in doc:
			tf[vocabulary_index[word]] += 1
		tf = [freq / doc_len for freq in tf]
		tf_idf = [tf[index] * idf[word] for word, index in vocabulary_index.items()]
		vectored_corpus.append(tf_idf)

	# calculate the distances between each line to find which are the closest.
	num_docs = len(vectored_corpus)# this is flawed, but I don't know what to do
	min_dist = float('inf')
	most_similar_pair = (-1, -1)
	for i in range(num_docs):
		for j in range(i + 1, num_docs):
			calc_dist = get_manh_dist(vectored_corpus[i], vectored_corpus[j])
			if calc_dist > min_dist: continue
			min_dist = calc_dist
			most_similar_pair = (i, j)

	print(most_similar_pair)


main(text)
