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
Filter the vocabulary fictionary to remove any stop words. Improves the
efficiency when only working with a dictionary with relevant words. The
stop words are from the NLTK corpus of stopwords.
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
Iterate through each txt file from both training directories of spam or 
nonspam. Create a dictionary with each unique word as a key and a count
for the unique word frequencies.
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
