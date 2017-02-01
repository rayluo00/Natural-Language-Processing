import os
import math
import NaiveBayes

def CalculateProb (dictionary, filteredDictionary, wordDictionary):
    condProbDict = {}
    denominator = sum(wordDictionary.values()) + 2500
    finalProb = math.log10(0.5)

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
        wordProb = condProbDict[word] ** wordExponent

        if wordProb > 0:
            finalProb = finalProb + math.log10(wordProb)

    return finalProb

def PerformTest (filteredDictionary, spamWordDictionary, nonspamWordDictionary):
    spamTestList = []
    nonspamTestList = []
    testList = [sorted(os.listdir('./spam-test')), sorted(os.listdir('./nonspam-test'))]
    dirPath = ['./spam-test/', './nonspam-test/']

    spamc = 0
    nonspamc = 0
    spamc2 = 0
    nonspamc2 = 0

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

            spamProb = CalculateProb(dictionary, filteredDictionary, spamWordDictionary)
            nonspamProb = CalculateProb(dictionary, filteredDictionary, nonspamWordDictionary)

            if spamProb > nonspamProb:
                if i == 0:
                    spamc = spamc + 1
                else:
                    spamc2 = spamc2 + 1
            else:
                if i == 0:
                    nonspamc = nonspamc + 1
                else:
                    nonspamc2 = nonspamc2 + 1

    print('SC: ',spamc, '| NSC: ',nonspamc)
    print('SC2: ',spamc2,'| NSC2: ',nonspamc2)

def Testing (filteredDictionary, spamWordDictionary, nonspamWordDictionary):
    PerformTest(filteredDictionary, spamWordDictionary, nonspamWordDictionary)
