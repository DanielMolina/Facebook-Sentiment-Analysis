import pdb

import logging, gensim, bz2
from gensim import corpora, models, similarities


logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

file_dir = 'data2/'

posts_file = open(file_dir + 'all_posts.txt', 'r')
posts = []

##############
# Load Posts #
##############
for line in posts_file:
	if line != '\n':
		message = line[:-1]
		posts.append(message)

posts_file.close()
##############

# remove common words and tokenize
stoplist = set('for a of the and to in this that it so'.split())
texts = [[word for word in post.lower().split() if word not in stoplist] for post in posts]

# remove words that only appear once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

# We use a document representation called "bag-of-words". 
# In this representation, each document is represented by one vector where each vector element
# represents a question-answer pair (i.e. "How many times does the word 'system' apper in the document? Once.").
# This is a mapping between questions and their ids.

dictionary = corpora.Dictionary(texts)
dictionary.save(file_dir + 'posts.dict')

# convert tokenized documents to vectors

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(file_dir + 'postcorpus.mm', corpus)





