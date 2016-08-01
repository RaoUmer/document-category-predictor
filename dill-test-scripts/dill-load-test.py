import dill
import re
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups

categories = ['comp.graphics', 'sci.space', 'rec.sport.hockey', 'soc.religion.christian', 'talk.politics.misc', 'rec.autos']
#data_test = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'), categories=categories)

clf = dill.load(open('classifier.dill', 'rb'))

data_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'), categories=categories)

# So, first converting text data into vectors of numerical values using tf-idf to form feature vector
vectorizer = TfidfVectorizer()
data_train_vectors = vectorizer.fit_transform(data_train.data)

Xtr = data_train_vectors

label = {0: 'computer', 1: 'science', 2: 'sports', 3: 'religion', 4: 'politics', 5: 'automobiles'}

#vectorizer = TfidfVectorizer()
#data_test_vectors = vectorizer.fit_transform(data_test.data)

X = data_train_vectors[1]

print "Prediction:", label[clf.predict(X)[0]]
