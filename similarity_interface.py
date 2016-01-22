import pdb

import logging, gensim, bz2
from gensim import corpora, models, similarities


logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

file_dir = 'data/'

# load corpus, dictionary, and lsi model
dictionary = corpora.Dictionary.load(file_dir + 'posts.dict')
corpus_lsi = corpora.MmCorpus(file_dir + 'corpus_lsi.mm')
lsi = models.LsiModel.load(file_dir + 'model.lsi')

# set up query as lsi vector
doc = 'smoking is bad'
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]
 
# initialize query structures and store it
index = similarities.MatrixSimilarity(corpus_lsi) # transforms corpus to lsi space and indexes it
index.save(file_dir + 'lsi.index')

# perform similarity queries
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key = lambda item: -item[1]) # sort similarities in descending order
# item from similarity list has form (document number, document similarity); -1 <= document similarity <= 1

# write results to file
sim_file = open(file_dir + 'similarity.txt', 'w')
sim_file.write(doc + '\n')
for item in sims:
	sim_file.write(str(item) + '\n')
sim_file.close()