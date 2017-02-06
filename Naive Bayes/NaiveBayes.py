'''
NaiveBayes.py

Authors: Raymond Weiming Luo
         Ben Ellerby

The program is trained by the training directory of spam and nonspam
to create a dictionary of which words are more frequent in a spam or
nonspam email. Additionally, the entire dictionary is composed of words
found in spam and nonspam emails of the training and testing set. Also,
a feature file can be created to map the document ID, word ID and word
frequencie.

'''

import os
import TestNaiveBayes
from collections import OrderedDict
from nltk.corpus import stopwords

#######################################################################################
'''
Get the names of all the txt files in each of the training directories.

list[0] = txt names from spam train
list[1] = txt names from nonspam train
list[2] = txt names from spam test
list[3] = txt names from nonspam test
'''
def GetFiles ():
    spamTrainList = sorted(os.listdir('./spam-train'))
    nonSpamTrainList = sorted(os.listdir('./nonspam-train'))
    spamTestList = sorted(os.listdir('./spam-test'))
    nonspamTestList = sorted(os.listdir('./nonspam-test'))

    return [spamTrainList, nonSpamTrainList, spamTestList, nonspamTestList]

#######################################################################################
'''
Filter out the stopwords from the vocabulary dictionary and limit the words
to the top 2500 frequent words.
'''
def FilterDictionary (wordDictionary):
    stopWords = set(stopwords.words('english'))
    tempDictionary = wordDictionary.copy()

    for key in wordDictionary:
        if key in stopWords:
            del tempDictionary[key]

    tempDictionary = OrderedDict(sorted(tempDictionary.items(), key=lambda t: t[1], reverse=True))
    finalDictionary = OrderedDict()

    c = 0
    for key in tempDictionary:
        if c > 2499:
            return finalDictionary
        else:
            finalDictionary.update({key:tempDictionary[key]})
        c = c + 1

    return finalDictionary

#######################################################################################
'''
Add the word into the dictionary if it doesn't contain it. A newly added
word has value 1, otherwise it increments the value by 1.
'''
def AddInDictionary (word, dictionary):
    if word not in dictionary:
        dictionary[word] = 1
    else:
        dictionary[word] = dictionary[word] + 1

    return dictionary

#######################################################################################
'''
Iterate through each txt file from the training directories. Create a 
dictionary with each unique word as a key and frequencies count.
'''
def CreateDictionary (emailList):
    spamTrain = []
    nonspamTrain = []
    wordDictionary = {}
    spamWordDictionary = {}
    nonspamWordDictionary = {}
    dirPath = ['./spam-train/', './nonspam-train/', './spam-test/', './nonspam-test/']

    for i in range(0, 4):
        emailListSz = len(emailList[i])
        for j in range(0, emailListSz):
            dictionary = {}
            txtFile = open(dirPath[i]+emailList[i][j], 'r')
            for line in txtFile:
                for word in line.split():
                    wordDictionary = AddInDictionary(word, wordDictionary)
                    dictionary = AddInDictionary(word, dictionary)

                    if i == 0:
                        spamWordDictionary = AddInDictionary(word, spamWordDictionary)
                    elif i == 1:
                        nonspamWordDictionary = AddInDictionary(word, nonspamWordDictionary)

            if i == 0:
                spamTrain.append(dictionary)
            elif i == 1:
                nonspamTrain.append(dictionary)

            txtFile.close()
    
    filteredDictionary = FilterDictionary(wordDictionary) 

    return filteredDictionary, spamWordDictionary, nonspamWordDictionary, spamTrain, nonspamTrain

#######################################################################################
'''
Find the index of the word in the ordered dictionary. Return index
of the word, else return -1 if the word isn't in the dictionary.
'''
def FindDictIndex (word, wordDictionary):
    if word not in wordDictionary:
        return -1
    
    index = 0
    for key in wordDictionary.keys():
        if key != word:
            index = index + 1
        else:
            return index

    return -1

#######################################################################################
'''
Convert the dictionary of words into the syntax of for a feature
file. Every word is replaced by the index in the dicitonary of all 
words.
'''
def ConvertFeatures (dictionary, wordDictionary):
    orderDictionary = {}

    for word in dictionary:
        idx = FindDictIndex(word, wordDictionary)
        if idx > -1:
            orderDictionary[idx] = dictionary[word]

    return OrderedDict(sorted(orderDictionary.items(), key=lambda t: t[0]))

#######################################################################################
'''
Write document ID, word and value into a txt file.
'''
def WriteToFile (docID, dictionary, outFile):
    for key in dictionary:
        outFile.write(str(docID)+' '+str(key)+' '+str(dictionary[key])+'\n')

#######################################################################################
'''
Find each word frequencies and convert the word to the index postion
of the word dictionary. Write output to the txt file.
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
    #FeatureFile(filteredDictionary, spamTrain, nonspamTrain)
    TestNaiveBayes.Testing(filteredDictionary, spamWordDictionary, nonspamWordDictionary, emailList)
