''' 
amazon_review.py

Author: Raymond Weiming Luo

Amazon review analysis using Naive Bayes and Support Vector Machine
classifiers. The classifiers are validated using k-folds, which is
currently implemented as 5-folds. The program splits the data to 
80% training and 20% testing.

'''

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
from test_amazon_review import TestNaiveBayes, TestSVM, Demo
from sklearn import svm

####################################################################
'''
Parse the json file and filter the data to have at most 300000 
data points, otherwise it would be highly computational for testing.
The data is also filtered to find unique products with 100+ reviews 
to improve reliability with the reviews.
'''
def ParseJSON ():
    data = []
    #filename = 'Amazon_Instant_Video_5.json'
    filename = 'Apps_for_Android_5.json'
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

    return data

####################################################################
'''
Split the data for each subset of the original data to a training set
and testing set. The testing data subset is iterative based on k-folds.
'''
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

####################################################################
'''
Add the word into the bag of words dictionary for each class.
'''
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

####################################################################
'''
Update the dictionary with the word for the specified class that is
associated with the rating of the review.
'''
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

####################################################################
'''
Train the classifier for Naive Bayes, each class has a bag of words
and all of the bag of words is created into a 5xN matrix. The 5 
represents each rating class and N is the size for the bag of words.
'''
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

####################################################################
'''
Train the LinearSVC on the training bag of words matrix and return
the classifier for Support Vector Machine.
'''
def TrainSVM (trainMatrix, scores):
    lin_svc = svm.LinearSVC(C=1.0).fit(trainMatrix, scores)
    return lin_svc

####################################################################
'''
Retrieve the data and split to a training and testing set. Perform
a k-fold validation for Naive Bayes and Support Vector Machine 
classification.
'''
if __name__ == '__main__':
    nb = 0
    svc = 0
    testCount = 0
    nbs1 = 0
    nbs2 = 0
    nbs3 = 0
    nbs4 = 0
    nbs5 = 0
    ss1 = 0
    ss2 = 0
    ss3 = 0
    ss4 = 0
    ss5 = 0
    data =  ParseJSON()
    random.shuffle(data)
    data_len = len(data)
    trainc = round(data_len * 0.8)
    testc = data_len - trainc

    mainNB, mainWordIndex, mainTrain, scores = TrainNaiveBayes(data)
    mainSVC = TrainSVM(mainTrain, scores)

    kfolds = math.ceil(data_len / testc)
    for i in range(0, kfolds):
        train, test = SplitData(data, i, trainc, testc, data_len)
        classifier, wordIndex, trainMatrix, scores = TrainNaiveBayes(train)
        word_len = len(wordIndex)
        ret_nb, ret_nbs1, ret_nbs2, ret_nbs3, ret_nbs4, ret_nbs5 = TestNaiveBayes(classifier, test, wordIndex, word_len)
        lin_svc = TrainSVM(trainMatrix, scores)
        ret_svc, ret_ss1, ret_ss2, ret_ss3, ret_ss4, ret_ss5 = TestSVM(lin_svc, trainMatrix, scores, test, wordIndex, word_len)
        testCount += len(test)
        
        nb += ret_nb
        nbs1 += ret_nbs1
        nbs2 += ret_nbs2
        nbs3 += ret_nbs3
        nbs4 += ret_nbs4
        nbs5 += ret_nbs5
        svc += ret_svc
        ss1 += ret_ss1
        ss2 += ret_ss2
        ss3 += ret_ss3
        ss4 += ret_ss4
        ss5 += ret_ss5

    print("FINAL NB:", nb/testCount)
    print("FINAL SVC:", svc/testCount,'\n')
    print("FINAL NB RATINGS:", nbs1/5, nbs2/5, nbs3/5, nbs4/5, nbs5/5)
    print("FINAL SVC RATINGS:", ss1/5,ss2/5,ss3/5,ss4/5,ss5/5)

    # Demo
    #Demo(mainWordIndex, len(mainWordIndex), mainSVC, mainNB)
