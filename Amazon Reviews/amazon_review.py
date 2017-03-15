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
from test_amazon_review import TestNaiveBayes, TestSVM
from sklearn import svm

def ParseJSON ():
    data = []
    filename = 'Amazon_Instant_Video_5.json'
    #filename = 'Apps_for_Android_5.json'
    #filename = 'Beauty_5.json'
    #filename = 'Digital_Music_5.json'
    #filename = 'Office_Products_5.json'
    productID = {}
    smallDataID = []
    reviewFilterRate = 100
    count = 0

    with open('./json/'+filename, 'r') as dataFile:
        for line in dataFile:
            if count == 300000:
                break
            d = json.loads(line)
            data.append(d)
            
            prodID = d['asin']
            if prodID not in productID:
                productID[prodID] = 1
            else:
                productID[prodID] = productID[prodID] + 1
            count += 1

    sz = len(data)
    if sz < 70000:
        multiplier = 1
    elif sz < 200000:
        multiplier = 2
    else:
        multiplier = 30

    reviewFilterRate = reviewFilterRate * multiplier

    for k in productID.keys():
        if productID[k] < reviewFilterRate:
            smallDataID.append(k)

    data = [d for d in data if d['asin'] not in smallDataID]
    print(filename,'| DATA SIZE:',len(data))

    return data

def SplitData (data, kfold, trainc, testc, data_len):
    testStart = kfold * testc
    testEnd = testStart + testc
    train = []
    test = []
    
    if testEnd > data_len:
        testEnd = data_len

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
            #else:
            #    d[word] = d[word] + 1

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

def TrainNaiveBayes (train):
    sz = len(train)
    stopWords = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    scores = [1,2,3,4,5]
    classifier = MultinomialNB(alpha=1.0)
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

    return classifier, wordIndex, trainMatrix, scores

def TrainSVM (trainMatrix, scores):
    lin_svc = svm.LinearSVC(C=1.0).fit(trainMatrix, scores)
    return lin_svc

if __name__ == '__main__':
    nb = 0
    svc = 0
    testCount = 0
    data =  ParseJSON()
    #data = data[:5000]
    random.shuffle(data)
    data_len = len(data)
    trainc = round(data_len * 0.8)
    testc = data_len - trainc

    kfolds = math.ceil(data_len / testc)

    for i in range(0, kfolds):
        train, test = SplitData(data, i, trainc, testc, data_len)
        classifier, wordIndex, trainMatrix, scores = TrainNaiveBayes(train)
        nb += TestNaiveBayes(classifier, test, wordIndex)
        lin_svc = TrainSVM(trainMatrix, scores)
        svc += TestSVM(lin_svc, trainMatrix, scores, test, wordIndex)
        testCount += len(test)

    print("FINAL NB:", nb/testCount)
    print("FINAL SVC:", svc/testCount,'\n')
