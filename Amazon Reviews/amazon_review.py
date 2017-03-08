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

def ParseJSON ():
    data = []
    filename = 'Amazon_Instant_Video_5.json'

    with open('./json/'+filename, 'r') as dataFile:
        data = [json.loads(line) for line in dataFile]

    return data

def SplitData (data):
    data_len = len(data)
    trainc = round(data_len * 0.70)
    testc = data_len - trainc

    random.shuffle(data)

    train = data[:trainc]
    test = data[trainc:]

    return train, test

def Train (train):
    sz = len(train)
    stopWords = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    scores = [1,2,3,4,5]
    classifer = MultinomialNB()

    for i in range(0, 10):
        overall = train[i]['overall']
        review = tokenizer.tokenize(train[i]['reviewText'].lower())
        #print(review)
        review = [word for word in review if word not in stopWords]
        #print(review,'\n')

if __name__ == '__main__':
    data =  ParseJSON()
    train ,test = SplitData(data)
    Train(train)
    #print(np.random.randint(20, size=(5, 100)))

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
