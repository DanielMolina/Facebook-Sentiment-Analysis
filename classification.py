import numpy
import pandas
import sklearn.cross_validation
import sklearn.feature_extraction.text
import sklearn.metrics
import sklearn.svm

import pdb

names = ['text', 'label']

# read in some text data
data = pandas.read_table('test_labels.txt', sep = '\t', names = names)

# split data into training and test (default sets 75% as training data)
train, test = sklearn.cross_validation.train_test_split(data)
train_data, test_data = pandas.DataFrame(train, columns = names), pandas.DataFrame(test, columns = names)

# vectorization is the process of converting all names into a binary vector
# of 1s and 0s such that the name is encoded as a set of on/off attributes
# for each n-gram
count_vectorizer = sklearn.feature_extraction.text.CountVectorizer(stop_words = 'english')
train_matrix = count_vectorizer.fit_transform(train_data['text'])
test_matrix = count_vectorizer.transform(test_data['text'])

# tfidf transformation
tfidf_transformer = sklearn.feature_extraction.text.TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_matrix)
test_tfidf = tfidf_transformer.transform(test_matrix)

# fit the model
classifier = sklearn.svm.SVC()
classifier.fit(train_matrix, train_data['label'])

# predict sentiment for the test set
predicted = classifier.predict(test_tfidf)

# calculate the diagnostics
accuracy = classifier.score(test_matrix, test_data['label'])
precision, recall, f1, _ = sklearn.metrics.precision_recall_fscore_support(test_data['label'], predicted)

print(' ')
print('Accuracy = ', accuracy)
print('Precision = ', precision)
print('Recall = ', recall)
print('F1 Score = ', f1)
