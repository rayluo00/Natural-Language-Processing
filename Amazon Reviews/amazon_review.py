from __future__ import division
import json
import math
import random
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

    random.shuffle(data)

    train = data[:trainc]
    test = data[trainc:]

    return train, test

def ProcessData (train):
    p1, p2, p3, p4, p5 = 0, 0, 0, 0, 0
    sz = len(train)
    stopWords = stopwords.words('english')

    for i in range(0, sz):
        # calculate prior
        overall = train[i]['overall']
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
    prior1, prior2, prior3, prior4, prior5 = ProcessData(train)

if __name__ == '__main__':
    data =  ParseJSON()
    train ,test = SplitData(data)
    Train(train)
