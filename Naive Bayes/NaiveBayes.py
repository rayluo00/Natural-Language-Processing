'''
NaiveBayes.py

Authors: Raymond Weiming Luo
         Ben Ellerby

'''

import os
from operator import itemgetter
from nltk.corpus import stopwords

#######################################################################################
'''
'''
def GetFiles ():
    spamTrainList = sorted(os.listdir('./spam-train'))
    nonSpamTrainList = sorted(os.listdir('./nonspam-train'))

    return [spamTrainList, nonSpamTrainList]

#######################################################################################
'''
'''
def FilterDictionary (wordDictionary):
    stopWords = set(stopwords.words('english'))
    tempDictionary = wordDictionary.copy()

    for key in wordDictionary:
        if key in stopWords:
            del tempDictionary[key]

    return tempDictionary

#######################################################################################
'''
'''
def ParseFiles (emailList):
    dirPath = ['./spam-train/', './nonspam-train/']

    wordDictionary = {}

    for i in range(0, 2):
        emailListSz = len(emailList[i])
        for j in range(0, emailListSz):
            txtFile = open(dirPath[i]+emailList[i][j], 'r')
            for line in txtFile:
                for word in line.split():
                    if word not in wordDictionary:
                        wordDictionary[word] = 1
                    else:
                        wordDictionary[word] = wordDictionary[word] + 1

    wordDictionary = FilterDictionary(wordDictionary)

    '''
    for key, value in sorted(wordDictionary.items(), key=itemgetter(1), reverse=True):
        print(key, value)
    '''

    return wordDictionary

if __name__ == '__main__':
    emailList = GetFiles()
    wordDictionary = ParseFiles(emailList)
