import pdb

import logging, gensim, bz2
from gensim import corpora, models, similarities


logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

file_dir = 'data2/'

# load corpus and dictionary
dictionary = corpora.Dictionary.load(file_dir + 'posts.dict')
corpus = corpora.MmCorpus(file_dir + 'postcorpus.mm')

# initialize tfidf model and apply it to the corpus and save them
tfidf = models.TfidfModel(corpus)
tfidf.save(file_dir + 'model.tfidf')
corpus_tfidf = tfidf[corpus]
corpora.MmCorpus.serialize(file_dir + 'corpus_tfidf.mm', corpus_tfidf)

# apply Latent Semantic Indexing (LSI) model to the tfidf corpus and save them
lsi = models.LsiModel(corpus_tfidf, id2word = dictionary, num_topics = 300)
lsi.save(file_dir + 'model.lsi')
corpus_lsi = lsi[corpus_tfidf]
corpora.MmCorpus.serialize(file_dir + 'corpus_lsi.mm', corpus_lsi)



