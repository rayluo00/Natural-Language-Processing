from __future__ import division
import json
import math
from pprint import pprint
from nltk.corpus import stopwords

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
    train = []
    test = []

    for d in range(0, data_len):
        if d < trainc:
            train.append(data[d])
        else:
            test.append(data[d])

    return train, test

def CalcPrior (train):
    p1, p2, p3, p4, p5 = 0, 0, 0, 0, 0
    sz = len(train)

    for d in train:
        overall = d['overall']
        if overall == 1.0:
            p1 += 1
        elif overall == 2.0:
            p2 += 1
        elif overall == 3.0:
            p3 += 1
        elif overall == 4.0:
            p4 += 1
        elif overall == 5.0:
            p5 += 1

    p1 = p1/sz
    p2 = p2/sz
    p3 = p3/sz
    p4 = p4/sz
    p5 = p5/sz

    return p1, p2, p3, p4, p5

def Train (train):
    train1, train2, train3, train4, train5 = ([] for i in range(5))
    stopWords = stopwords.words('english')
    prior1, prior2, prior3, prior4, prior5 = CalcPrior(train)

if __name__ == '__main__':
    data =  ParseJSON()
    train ,test = SplitData(data)
    Train(train)
