# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 22:24:10 2017

@author: bibigul
"""

# Dependencies

import pandas as pd  # for reading csvs

# imports from sklearn to make our classifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

# for cleaning our text
import nltk
import string
import random
import matplotlib.pyplot as plt
from collections import Counter

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


# First, read the genre csv file
# available for now at https://s3.amazonaws.com/pyshakespeare/genre.csv
df = pd.DataFrame.from_csv("shake_genres4.csv")


# I've included the "play" and "citation" columns just for kicks.
# We only really need the "text" and "genre" columns.
speeches = list(df['text'])
labels = list(df['genre'])
plays = list(df['play'])

#
#letter_counts = Counter(labels)
#df1 = pd.DataFrame.from_dict(letter_counts, orient='index')
#ax = df1.sort(columns=0, ascending = False).plot(kind='bar', title="Histogram of scenes categories", legend = 'False', colormap = 'jet')
#ax.set_ylabel("# of instances")
#plt.tight_layout()
#
#letter_counts2 = Counter(plays)
#df2 = pd.DataFrame.from_dict(letter_counts2, orient='index')
#ax = df2.sort(columns=0, ascending = False).plot(kind='bar', title="Histogram of scenes in plays", legend = 'False', colormap = 'jet')
#ax.set_ylabel("# of instances")
#ax.set_xlabel("plays")
#plt.tight_layout()


test_size = int(len(speeches) * 0.2)
all_ind = range(0, len(speeches))
unused_ind = all_ind
NBC_score = 0
#SVC_score = 0
#cnf_matrix = [[0,0,0], [0,0,0], [0,0,0]]

for i in range(0, 5):

    # Now, we want to divide our data into two groups
    # The first for training our classifer, and the second to test its accuracy
    test_ind = random.sample(unused_ind, test_size)
    training_ind = list(set(all_ind)-set(test_ind))
    unused_ind = list(set(unused_ind)-set(test_ind))
    
    # the training speeches and labels should have the bulk of the data
    train_speeches = list(speeches[i] for i in training_ind)
    train_labels = list(labels[i] for i in training_ind)
    
    test_speeches = list(speeches[i] for i in test_ind)
    test_labels = list(labels[i] for i in test_ind)
    
    # To do that, we use the CountVectorizor
    vectorizer = CountVectorizer()
    
    # first, we "teach" the vectorizor which tokens to vectorize on
    vectorizer.fit(train_speeches)
    # then we vectorize those speeches
    train_features = vectorizer.transform(train_speeches)
    
    test_features = vectorizer.transform(test_speeches)
    
    
    classifier = MultinomialNB()
    classifier.fit(train_features, train_labels)
#    predict_labels = classifier.predict(test_features)
#    cnf_matrix += confusion_matrix(test_labels, predict_labels)
    
    NBC_score+= classifier.score(test_features, test_labels)
    
#   classifier = SVC(kernel='linear')
#    classifier.fit(train_features, train_labels)
#    
#    SVC_score+= classifier.score(test_features, test_labels)

#print cnf_matrix
NBC_score /= 5
print NBC_score
#SVC_score /= 5
#print SVC_score