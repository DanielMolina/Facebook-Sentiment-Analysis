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
stoplist = set("""a about above after again against all am an and any are aren't as at be because been before being 
below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for
from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself 
his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor 
not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should 
shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll
they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what
what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll 
you're you've your yours yourself yourselves""".split())
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





