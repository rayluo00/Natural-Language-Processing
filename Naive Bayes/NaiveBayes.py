'''
NaiveBayes.py

Authors: Raymond Weiming Luo
         Ben Ellerby

'''

import os
import TestNaiveBayes
from collections import OrderedDict
from nltk.corpus import stopwords

#######################################################################################
'''
Get the names of all the txt files in each of the training directories.
Return a list containing the list of txt file names.

list[0] = list of txtx file names from the spam training directory
list[1] = list of txt file names from the nonspam training directory
'''
def GetFiles ():
    spamTrainList = sorted(os.listdir('./spam-train'))
    nonSpamTrainList = sorted(os.listdir('./nonspam-train'))

    return [spamTrainList, nonSpamTrainList]

#######################################################################################
'''
Filter the vocabulary dictionary to modify the stop words by decreasing 
their relevance. Improves the efficiency when only working with a 
dictionary with relevant words. The stop words are from the NLTK corpus 
of stopwords.
'''
def FilterDictionary (wordDictionary):
    stopWords = set(stopwords.words('english'))
    tempDictionary = wordDictionary.copy()

    for key in wordDictionary:
        if key in stopWords:
            del tempDictionary[key]
            #tempDictionary[key] = 0

    tempDictionary = OrderedDict(sorted(tempDictionary.items(), key=lambda t: t[1], reverse=True))
    finalDictionary = tempDictionary.copy()

    c = 0
    for key in tempDictionary:
        if c > 2499:
            del finalDictionary[key]
        c = c + 1

    return finalDictionary

def AddInDictionary (word, dictionary):
    if word not in dictionary:
        dictionary[word] = 1
    else:
        dictionary[word] = dictionary[word] + 1

    return dictionary

#######################################################################################
'''
Iterate through each txt file from both training directories of spam or 
nonspam. Create a dictionary with each unique word as a key and a count
for the unique word frequencies.
'''
def CreateDictionary (emailList):
    spamTrain = []
    nonspamTrain = []
    wordDictionary = {}
    spamWordDictionary = {}
    nonspamWordDictionary = {}
    dirPath = ['./spam-train/', './nonspam-train/']

    for i in range(0, 2):
        emailListSz = len(emailList[i])
        for j in range(0, emailListSz):
            dictionary = {}
            txtFile = open(dirPath[i]+emailList[i][j], 'r')
            for line in txtFile:
                for word in line.split():
                    wordDictionary = AddInDictionary(word, wordDictionary)
                    dictionary = AddInDictionary(word, dictionary)

                    if i % 2 == 0:
                        spamWordDictionary = AddInDictionary(word, spamWordDictionary)
                    else:
                        nonspamWordDictionary = AddInDictionary(word, nonspamWordDictionary)

            if i % 2 == 0:
                spamTrain.append(dictionary)
            else:
                nonspamTrain.append(dictionary)
            txtFile.close()

    
    filteredDictionary = FilterDictionary(wordDictionary) 

    return filteredDictionary, spamWordDictionary, nonspamWordDictionary, spamTrain, nonspamTrain

#######################################################################################
'''
'''
def FindDictIndex (word, wordDictionary):

    if word not in wordDictionary:
        return -1

    index = 0

    for key in wordDictionary:
        if key != word:
            index = index + 1
        else:
            return index

    return -1

#######################################################################################
'''
'''
def ConvertFeatures (dictionary, wordDictionary):
    orderDictionary = {}

    for word in dictionary:
        #print(word+'|'+str(dictionary[word]))
        idx = FindDictIndex(word, wordDictionary)
        if idx != -1:
            orderDictionary[idx] = dictionary[word]

    #print('---------------------------------------------------------\n')

    return OrderedDict(sorted(orderDictionary.items(), key=lambda t: t[0]))

#######################################################################################
'''
'''
def WriteToFile (docID, dictionary, outFile):
    for key in dictionary:
        outFile.write(str(docID)+' '+str(key)+' '+str(dictionary[key])+'\n')

#######################################################################################
'''
'''
def FeatureFile (filteredDictionary, spamTrain, nonspamTrain):
    try: 
        spamFile = open('spam-features.txt', 'w+')
        nonspamFile = open('nonspam-features.txt', 'w+')
        dictionaryFile = open('dictionary.txt', 'w+')
    except IOError:
        print('ERROR: I/O exception when opening features.txt')

    docID = 0
    for word in filteredDictionary:
        dictionaryFile.write(str(docID)+' '+word+' '+str(filteredDictionary[word])+'\n')
        docID = docID + 1

    docID = 1
    for dictionary in nonspamTrain:
        dictionary = ConvertFeatures(dictionary, filteredDictionary)
        WriteToFile(docID, dictionary, nonspamFile)
        docID = docID + 1

    docID = 1
    for dictionary in spamTrain:
        dictionary = ConvertFeatures(dictionary, filteredDictionary)
        WriteToFile(docID, dictionary, spamFile)
        docID = docID + 1

    spamFile.close()
    nonspamFile.close()
    dictionaryFile.close()

if __name__ == '__main__':
    emailList = GetFiles()
    filteredDictionary, spamWordDictionary, nonspamWordDictionary, spamTrain, nonspamTrain = CreateDictionary(emailList)
    FeatureFile(filteredDictionary, spamTrain, nonspamTrain)
    TestNaiveBayes.Testing(filteredDictionary, spamWordDictionary, nonspamWordDictionary)
