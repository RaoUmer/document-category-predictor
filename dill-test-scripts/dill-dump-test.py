import dill
import os
import re
import pandas as pd
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.datasets import fetch_20newsgroups

stop = stopwords.words('english')


categories = ['comp.graphics', 'sci.space', 'rec.sport.hockey', 'soc.religion.christian', 'talk.politics.misc', 'rec.autos']
#categories = None
data_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'), categories=categories)

# So, first converting text data into vectors of numerical values using tf-idf to form feature vector
vectorizer = TfidfVectorizer()
data_train_vectors = vectorizer.fit_transform(data_train.data)

Xtr = data_train_vectors
ytr = data_train.target

# Implementing classification model- using LinearSVC
# Instantiate the estimator
clf =  LinearSVC(C=1, tol=0.01)
# Fit the model with data (aka "model training")
clf.fit(Xtr, ytr)


dill.dump(stop,
            open('stopwords.dill', 'wb'),
            protocol=2)

dill.dump(clf,
            open('classifier.dill', 'wb'),
            protocol=2)
