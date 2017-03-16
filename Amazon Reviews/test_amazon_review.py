from __future__ import division
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

stopWords = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

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
