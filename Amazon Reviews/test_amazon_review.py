'''
test_amazon_review.pg

Author: Raymond Weiming Luo

Testing program to validate the pass rate for the Naive Bayes and 
Support Vector Machine classifiers. The validation is for the 
testing dataset.

'''

from __future__ import division
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

stopWords = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

####################################################################
'''
Test each review from the Naive Bayes classifier in the testing set
to compare the accuracy with the generated rating with the actual 
review.
'''
def TestNaiveBayes (classifier, test, wordIndex, word_len):
    sz = len(test)
    passCount = 0

    for i in range(0, sz):
        overall = int(test[i]['overall'])
        review = tokenizer.tokenize(test[i]['reviewText'].lower())
        review = [word for word in review if word not in stopWords and word in wordIndex]
        review.sort()
        
        testcase = [0 for i in range(word_len)]
        for word in review:
            testcase[wordIndex.index(word)] += 1

        testcase = np.array(testcase).reshape(1, -1)
        rating = classifier.predict(testcase)[0]
        
        if (rating == overall):
            passCount += 1

    print("NB PASS:", passCount/sz)
    return passCount

####################################################################
'''
Test each review from the Support Vector Machine classifier in the 
testing set and compare the accuracy of the generated rating with 
the actual rating.
'''
def TestSVM (lin_svc, trainMatrix, scores, test, wordIndex, word_len):
    sz = len(test)
    passCount = 0

    for i in range(0, sz):
        overall = int(test[i]['overall'])
        review = tokenizer.tokenize(test[i]['reviewText'].lower())
        review = [word for word in review if word not in stopWords and word in wordIndex]
        review.sort()
        
        testcase = [0 for i in range(word_len)]
        for word in review:
            testcase[wordIndex.index(word)] += 1

        testcase = np.array(testcase).reshape(1, -1)
        rating = lin_svc.predict(testcase)[0]
        
        if (rating == overall):
            passCount += 1

    print("SVM PASS:", passCount/sz,'\n')
    return passCount

####################################################################
'''
Demo function to recieve the text for a review as input and print the
generated rating for Naive Bayes and Support Vector Machine.
'''
def Demo (wordIndex, word_len, lin_svc, classifier):

    while True:
        review = input('$ ')

        review = tokenizer.tokenize(review.lower())
        review = [word for word in review if word not in stopWords and word in wordIndex]
        review.sort()

        testcase = [0 for i in range(word_len)]
        for word in review:
            testcase[wordIndex.index(word)] += 1

        testcase = np.array(testcase).reshape(1, -1)

        nbRating = classifier.predict(testcase)[0]
        svcRating = lin_svc.predict(testcase)[0]

        print('\nNaive Bayes Rating:',nbRating,
                '\nSupport Vector Machine Rating:',svcRating)
