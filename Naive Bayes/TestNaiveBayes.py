'''
TestNaiveBayes.py

Authors: Raymond Weiming Luo
         Ben Ellerby

'''

import os
import math
import NaiveBayes

#######################################################################################
'''
Calculate the probrability of the given dictionary to determine if the
dictionary is a spam or nonspam email. The probrability is an 
implementation of the Naive Bayes theorem.
'''
def CalculateProb (dictionary, filteredDictionary, wordDictionary, prior):
    condProbDict = {}
    finalProb = math.log10(prior)
    denominator = sum(wordDictionary.values()) + 2500

    for word in dictionary.keys():
        if word not in wordDictionary:
            wordCount = 0
        else:
            wordCount = wordDictionary[word]
        wordCount = wordCount + 1
        
        conditionalProb = wordCount / denominator
        condProbDict[word] = conditionalProb

    for word in dictionary.keys():
        wordExponent = dictionary[word]
        wordProb = (condProbDict[word] ** wordExponent)

        if wordProb > 0:
            finalProb = finalProb + math.log10(wordProb)

    return finalProb

#######################################################################################
'''
Testing function to go through the testing set and determine if the file is a 
spam or nonspam email. Output the 2x2 positive/negative table, precision, 
recall, and f-value.
'''
def Testing (filteredDictionary, spamWordDictionary, nonspamWordDictionary, emailList):
    tp = 0
    fn = 0
    fp = 0
    tn = 0
    testList = [sorted(os.listdir('./spam-test')), sorted(os.listdir('./nonspam-test'))]
    dirPath = ['./spam-test/', './nonspam-test/']
    spamTrainSize = len(emailList[0])
    nonspamTrainSize = len(emailList[1])
    totalTrainSize = spamTrainSize + nonspamTrainSize
    spamPrior = spamTrainSize / totalTrainSize
    nonspamPrior = nonspamTrainSize / totalTrainSize

    for i in range(0, 2):
        testListSize = len(testList[i])
        for j in range(0, testListSize):
            dictionary = {}
            txtFile = open(dirPath[i]+testList[i][j], 'r')
            for line in txtFile:
                for word in line.split():
                    if word not in dictionary:
                        dictionary[word] = 1
                    else:
                        dictionary[word] = dictionary[word] + 1

            txtFile.close()

            spamProb = CalculateProb(dictionary, filteredDictionary, 
                    spamWordDictionary, spamPrior)
            nonspamProb = CalculateProb(dictionary, filteredDictionary, 
                    nonspamWordDictionary, nonspamPrior)

            if spamProb > nonspamProb:
                if i == 0:
                    tp = tp + 1
                else:
                    fn = fn + 1
            else:
                if i == 0:
                    fp = fp + 1
                else:
                    tn = tn + 1

    print('        ---------------------')
    print('SPAM    | tp: {:>3} | fp: {:>3} |'.format(tp,fp))
    print('        ---------------------')
    print('NONSPAM | fn: {:>3} | tn: {:>3} |'.format(fn,tn))
    print('        ---------------------\n')

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fscore = (2 * precision * recall) / (precision + recall)

    print('precision: %.5f' % precision)
    print('recall   : %.5f' % recall)
    print('f-score  : %.5f' % fscore)
