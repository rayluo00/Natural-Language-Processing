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
    #stopWords = set(stopwords.words('english'))
    tempDictionary = wordDictionary.copy()

    for key in wordDictionary:
        #if key in stopWords:
        if len(key) < 3:
            del tempDictionary[key]
            #tempDictionary[key] = 0

    return tempDictionary

#######################################################################################
'''
Iterate through each txt file from both training directories of spam or 
nonspam. Create a dictionary with each unique word as a key and a count
for the unique word frequencies.
'''
def CreateDictionary (emailList):
    wordDictionary = {}
    dirPath = ['./spam-train/', './nonspam-train/']

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
            txtFile.close()

    wordDictionary = FilterDictionary(wordDictionary)
    wordDictionary = OrderedDict(sorted(wordDictionary.items(), key=lambda t: t[1], reverse=True))
    
    '''
    c = 0
    for key, value in wordDictionary.items():
        c = c + 1
        #if c == 46:
        #    print('-------------------------> ',key, value)
        print(key, value)
    '''

    return wordDictionary

#######################################################################################
'''
'''
def FindDictIndex (word, wordDictionary):
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
def FeatureFile (wordDictionary, emailList):
    dirPath = ['./spam-train/', './nonspam-train/']

    try:
        if os.path.exists('spam-features.txt'):
            os.remove('spam-features.txt')
        if os.path.exists('nonspam-features.txt'):
            os.remove('nonspam-features.txt')
        
        spamFile = open('spam-features.txt', 'w+')
        nonspamFile = open('nonspam-features.txt', 'w+')

        for i in range(1, 2):
            emailListSz = len(emailList[i])
            for j in range(0, emailListSz):
                dictionary = {}
                txtFile = open(dirPath[i]+emailList[i][j], 'r')
                for line in txtFile:
                    for word in line.split():
                        dictIndex = FindDictIndex(word, wordDictionary)
                        if dictIndex != -1:
                            if dictIndex not in dictionary:
                                dictionary[dictIndex] = 1
                            else:
                                dictionary[dictIndex] = dictionary[dictIndex] + 1
                
                txtFile.close()

                dictionary = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

                for key, value in dictionary.items():
                    c = 0
                    for word in wordDictionary:
                        if c == key:
                            x = word
                            break
                        c = c + 1

                    print(key, value, x)
                print('\n------------------------------------------------------\n')

        spamFile.close()
        nonspamFile.close()
    except IOError:
        print('ERROR: I/O exception when opening features.txt')

if __name__ == '__main__':
    emailList = GetFiles()
    wordDictionary = CreateDictionary(emailList)
    FeatureFile(wordDictionary, emailList)
