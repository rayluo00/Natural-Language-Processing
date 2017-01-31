'''
NaiveBayes.py

Authors: Raymond Weiming Luo
         Ben Ellerby

'''

import os
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
        if c > 2500:
            del finalDictionary[key]
        c = c + 1

    return finalDictionary

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
    dirPath = ['./spam-train/', './nonspam-train/']

    for i in range(0, 2):
        emailListSz = len(emailList[i])
        for j in range(0, emailListSz):
            dictionary = {}
            txtFile = open(dirPath[i]+emailList[i][j], 'r')
            for line in txtFile:
                for word in line.split():
                    if word not in wordDictionary:
                        wordDictionary[word] = 1
                    else:
                        wordDictionary[word] = wordDictionary[word] + 1

                    if word not in dictionary:
                        dictionary[word] = 1
                    else:
                        dictionary[word] = dictionary[word] + 1

            if i % 2 == 0:
                spamTrain.append(dictionary)
            else:
                nonspamTrain.append(dictionary)
            txtFile.close()

    wordDictionary = FilterDictionary(wordDictionary)
    
    '''
    c = 0
    for key, value in wordDictionary.items():
        c = c + 1
        #if c == 46:
        #    print('-------------------------> ',key, value)
        print(key, value)
    '''

    return wordDictionary, spamTrain, nonspamTrain

#######################################################################################
'''
'''
def FindDictIndex (word, wordDictionary):
    index = 0

    if word not in wordDictionary:
        return -1

    for key in wordDictionary:
        if key != word:
            index = index + 1
        else:
            return index

    return -1

def ConvertFeatures (dictionary, wordDictionary):
    orderDictionary = {}

    for word in dictionary:
        idx = FindDictIndex(word, wordDictionary)
        if idx != -1:
            orderDictionary[idx] = dictionary[word]

    return OrderedDict(sorted(orderDictionary.items(), key=lambda t: t[0]))

def WriteToFile (docID, dictionary, outFile):
    for key in dictionary:
        outFile.write(str(docID)+' '+str(key)+' '+str(dictionary[key])+'\n')

#######################################################################################
'''
'''
def FeatureFile (wordDictionary, spamTrain, nonspamTrain):
    try:
        if os.path.exists('spam-features.txt'):
            os.remove('spam-features.txt')
        if os.path.exists('nonspam-features.txt'):
            os.remove('nonspam-features.txt')
        
        spamFile = open('spam-features.txt', 'w+')
        nonspamFile = open('nonspam-features.txt', 'w+')
    except IOError:
        print('ERROR: I/O exception when opening features.txt')

    docID = 1
    for dictionary in nonspamTrain:
        dictionary = ConvertFeatures(dictionary, wordDictionary)
        WriteToFile(docID, dictionary, nonspamFile)
        docID = docID + 1

    docID = 1
    for dictionary in spamTrain:
        dictionary = ConvertFeatures(dictionary, wordDictionary)
        WriteToFile(docID, dictionary, spamFile)
        docID = docID + 1

    spamFile.close()
    nonspamFile.close()

if __name__ == '__main__':
    emailList = GetFiles()
    wordDictionary, spamTrain, nonspamTrain = CreateDictionary(emailList)
    FeatureFile(wordDictionary, spamTrain, nonspamTrain)
