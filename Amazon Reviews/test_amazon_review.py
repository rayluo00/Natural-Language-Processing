from __future__ import division
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def TestNaiveBayes (classifier, test, wordIndex):
    sz = len(test)
    word_len = len(wordIndex)
    stopWords = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
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

def TestSVM (lin_svc, trainMatrix, scores, test, wordIndex):
    sz = len(test)
    passCount = 0
    stopWords = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    word_len = len(wordIndex)

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
