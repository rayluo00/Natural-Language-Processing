from __future__ import division
import json
import math
import random
import numpy as np
from pprint import pprint
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
from test_amazon_review import Test

def ParseJSON ():
    data = []
    filename = 'Amazon_Instant_Video_5.json'

    with open('./json/'+filename, 'r') as dataFile:
        data = [json.loads(line) for line in dataFile]

    return data

def SplitData (data, kfold, trainc, testc, data_len):
    testStart = kfold * testc
    testEnd = testStart + testc
    train = []
    test = []
    print(testStart, testEnd)

    for i in range(0, data_len):
        if i >= testStart and i < testEnd:
            test.append(data[i])
        else:
            train.append(data[i])

    return train, test

def AddWord (dictionaries, idx, word):
    for i in range(0, 5):
        d = dictionaries[i]
        if idx == i:
            if word not in d:
                d[word] = 1
            else:
                d[word] = d[word] + 1
        else:
            if word not in d:
                d[word] = 0
            else:
                d[word] = d[word] + 1

def UpdateDict (dictionaries, overall, review):
    for word in review:
        if overall == 1.0:
            AddWord(dictionaries, 0, word)
        elif overall == 2.0:
            AddWord(dictionaries, 1, word)
        elif overall == 3.0:
            AddWord(dictionaries, 2, word)
        elif overall == 4.0:
            AddWord(dictionaries, 3, word)
        else:
            AddWord(dictionaries, 4, word)

def Train (train):
    sz = len(train)
    stopWords = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    scores = [1,2,3,4,5]
    classifier = MultinomialNB()
    dictionaries = [{} for i in range(5)]
    trainBagOfWords = []
    wordIndex = []

    for i in range(0, sz):
        overall = train[i]['overall']
        review = tokenizer.tokenize(train[i]['reviewText'].lower())
        review = [word for word in review if word not in stopWords]
        UpdateDict(dictionaries,overall,review)

    for j in range(0, 5):
        d = dictionaries[j]
        dictionaries[j] = OrderedDict(sorted(d.items(), key=lambda x: x[0]))

    for word in dictionaries[1].keys():
        wordIndex.append(word)

    for od in dictionaries:
        trainBagOfWords.append([k for k in od.values()])

    trainMatrix = np.array(trainBagOfWords)
    classifier.fit(trainMatrix, scores)

    return classifier, wordIndex

if __name__ == '__main__':
    data =  ParseJSON()
    data = data[:8000]
    random.shuffle(data)
    data_len = len(data)
    trainc = round(data_len * 0.8)
    testc = data_len - trainc

    kfolds = data_len // testc

    for i in range(0, kfolds):
        train, test = SplitData(data, i, trainc, testc, data_len)
        classifier, wordIndex = Train(train)
        Test(classifier, test, wordIndex)

    # EXAMPLE
    '''
    X = np.random.randint(20, size=(5, 100))
    y = np.array(['r1','r2','r3','r4','r5'])
    clf = MultinomialNB()
    clf.fit(X,y)
    print(X,'\n')
    x1 = np.random.randint(20, size=(1,100))
    x2 = np.random.randint(20, size=(1,100))
    x3 = np.random.randint(20, size=(1,100))
    print(clf.predict(x1))
    print(clf.predict(x2))
    print(clf.predict(x3))
    '''
