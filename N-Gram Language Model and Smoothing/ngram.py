import nltk

n = 2 # bigrams

# assumes start/end symbol preprocessing (via sed)
f = open("./train.txt").read().split()
fdist = nltk.FreqDist(f)
words = [word if fdist[word] > 1 else '<UNK>' for word in f]
fdist_replace = nltk.FreqDist(words)
ngrams_cfd = nltk.ConditionalFreqDist(nltk.ngrams(words, n))
ngrams_cpd = nltk.ConditionalProbDist(ngrams_cfd, nltk.MLEProbDist)


def generate(length):
    sentence = ['<s>']
    for i in range(length):
        sentence.append(ngrams_cpd[sentence[i]].generate())
    sentence.append('</s>')
    print(sentence)
    return sentence

def oneprob(word):
    return fdist_replace[word] / len(fdist_replace) 

def calcprob(sentence):
    prob = oneprob(sentence[1]) # ignore index 0, the <s>
    for i in range(2,(len(sentence) - 2)): # ignore last index, the </s>, and last word of sentence (caught by i+1, prevent index error)
        prob *= ngrams_cpd[sentence[i]].prob(sentence[i+1])
    print(prob)
    return prob

calcprob(generate(10))

