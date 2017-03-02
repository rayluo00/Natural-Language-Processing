'''
vtag.py

Author: Ben Ellerby & Raymond Weiming Luo

This program is to determine the part-of-speech tagging using
the VIterbi algorithm. The data are trained to find the most
commonly associated tag for a given word. This program takes 
two arguments, where arg[1] is the name of the training set 
and arg[2] is the name of the testing set.

'''

from __future__ import division
import math
import sys
from sys import argv

if len(argv) < 3:
        print('not enough arguments')
        sys.exit(0)

if argv[1] == 'entrain':
        f = open("data/en/entrain.txt").read().split()
        f_raw = open("data/en/enraw.txt").read().split()
elif argv[1] == 'ic2train' or argv[1] == 'ictrain':
        f = open("data/ic/"+argv[1]+".txt").read().split()
        f_raw = []
else:
        print('invalid txt file')
        sys.exit(0)

l = []
all_words = []
word_tag_counts = {}
tag_counts = {}
cond_tag_counts = {}
total_word_count = 0
tag_tag_sing = {}
word_tag_sing = {}

# train
for line in f:
        l.append(line.split("/"))

for line in l:
        all_words.append(line[0])

        if line[0] not in word_tag_counts:
                word_tag_counts[line[0]] = {line[1]: 1}
                word_tag_sing[line[1]] = word_tag_sing.get(line[1], 0) + 1
        else:
                if line[1] not in word_tag_counts[line[0]]:
                        word_tag_counts[line[0]][line[1]] = 1
                        word_tag_sing[line[1]] = word_tag_sing.get(line[1], 0) + 1
                else:
                        word_tag_counts[line[0]][line[1]] += 1
                        if word_tag_counts[line[0]][line[1]] == 2:
                                word_tag_sing[line[1]] -= 1

raw_words = []
for line in f_raw:
        raw_words.append(line)
        all_words.append(line)

for i in range(len(l)):
        current = l[i][1]
        # number of times each tag appears
        if current not in tag_counts:
                tag_counts[current] = 1
        else:
                tag_counts[current] += 1
        # number of times each previous tag sequence appears
        if i > 0:
                prev = l[i-1][1]
                if current not in cond_tag_counts:
                        cond_tag_counts[current] = {prev: 1}
                        tag_tag_sing[prev] = tag_tag_sing.get(prev, 0) + 1
                else:
                        if prev not in cond_tag_counts[current]:
                                cond_tag_counts[current][prev] = 1
                                tag_tag_sing[prev] = tag_tag_sing.get(prev, 0) + 1
                        else:
                                cond_tag_counts[current][prev] += 1
                                if cond_tag_counts[current][prev] == 2:
                                        tag_tag_sing[prev] -= 1

all_tags = []
everyTag = []
# get all unique tag referenced and every tag references
for x in word_tag_counts.keys():
        for t in word_tag_counts[x]:
                everyTag.append(t)

                if t not in all_tags:
                        all_tags.append(t)

# compute the total of all the words in the training corpus
for d in word_tag_counts.values():
        total_word_count += sum(d.values())

# compute the count of all unique tags for each word that is referenced at most once
unique_tag_words = {}
for w in word_tag_counts.keys():
        for t in word_tag_counts[w]:
                if word_tag_counts[w][t] == 1:
                        if t not in unique_tag_words:
                                unique_tag_words[t] = 1
                        else:
                                unique_tag_words[t] += 1

# singleton functions
def word_tag_sing_count(tag):
        return word_tag_sing[tag]

def tag_tag_sing_count(tag):
        return tag_tag_sing[tag]

# probability helper functions
def prob_tag_given_word(tag, word):
        smooth = 1
        denom = len(everyTag)

        if word not in word_tag_counts.keys():
                return math.log(smooth / len(all_words))
        if tag in word_tag_counts[word].keys():
                smooth += word_tag_counts[word][tag]
        
        # num times tag assoc w/ word / num times word appears total
        return math.log(smooth / denom)

def prob_word_given_tag(tag, word):
        denom = total_word_count
        # Bayes' theorem
        if tag == '###' and word == '###':
            return 1
        if word not in word_tag_counts.keys():
                return prob_tag_given_word(tag, word) + math.log((1 / denom))
        return prob_tag_given_word(tag, word) + math.log((sum(word_tag_counts[word].values()) / denom))

def prob_tag_given_tag(current, prev):
        if prev not in cond_tag_counts[current].keys():
                #old smoothing
                return math.log(1 / len(cond_tag_counts[current].keys()))
        return math.log((cond_tag_counts[current][prev])+1) - math.log(sum(cond_tag_counts[current].values()))

def tag_dict(word):
        if word not in word_tag_counts.keys():
                return all_tags
        return word_tag_counts[word].keys()

# calculate the singleton of tag given tag
def calc_tt_singleton(tag):
        count_unique = 1

        for k in cond_tag_counts.keys():
            if tag in cond_tag_counts[k] and cond_tag_counts[k][tag] == 1:
                count_unique += 1 

        return count_unique

# probrability of current tag given previous tag
def prob_tt(current, prev):
        # nums of prev tags associated with current tag
        if prev not in cond_tag_counts[current].keys():
                count_tt = 0
        else:
                count_tt = cond_tag_counts[current][prev]
        
        # nums of prev tags in the training corpus
        if prev not in cond_tag_counts.keys():
                count_t = 0
        else:
                count_t = sum(cond_tag_counts[prev].values())

        # lambda
        lmda = calc_tt_singleton(prev)

        # backoff
        backoff = 1
        if current in tag_counts:
            backoff = tag_counts[current] / total_word_count

        return math.log((count_tt + lmda * backoff) / (count_t + lmda))

# calculate the singleton for tag given word
def calc_tw_singleton(tag):
        count_unique = 1
        if tag not in unique_tag_words:
                return count_unique
        else:
                count_unique += unique_tag_words[tag]

        return count_unique

# probrability of tag given word
def prob_wt(tag, word):
        # num of tag associated with current word
        if word not in word_tag_counts:
                count_tw = 0
        else:
                count_tw = word_tag_counts[word][tag]

        # num of tag reference in training corpus
        if tag not in cond_tag_counts.keys():
                count_t = 0
        else:
                count_t = sum(cond_tag_counts[tag].values())

        # lambda
        lmda = calc_tw_singleton(tag)

        # backoff
        backoff = 1
        if word in word_tag_counts:
                backoff = (sum(word_tag_counts[word].values()) + 1) / (total_word_count + len(all_tags))

        return math.log((count_tw + lmda * backoff) / (count_t + lmda))

# prepare test data
if argv[2] == 'entest':
    test = open("data/en/entest.txt").read().split()
elif argv[2] == 'ic2test' or argv[2] == 'ictest':
    test = open("data/ic/"+argv[2]+".txt").read().split()

words = [l.split("/")[0] for l in test]
tags = [l.split("/")[1] for l in test]

# viterbi
mu = {k:[float('-inf') for x in range(len(words))] for k in tag_counts.keys()}
mu['###'][0] = 0.0
backpointer = ['*' for x in range(len(words))]

mu2 = {k:[float('-inf') for x in range(len(words))] for k in tag_counts.keys()}
mu2['###'][0] = 0.0
backpointer2 = ['*' for x in range(len(words))]

for i in range(1, len(words)):
        for current_tag in tag_dict(words[i]):
                for prev_tag in tag_dict(words[i-1]):
                        # original viterbi algorithm
                        p = prob_tag_given_tag(current_tag, prev_tag) + prob_word_given_tag(current_tag, words[i])
                        new_mu = mu[prev_tag][i-1] + p
                        if new_mu > mu[current_tag][i]:
                                mu[current_tag][i] = new_mu
                                backpointer[i] = prev_tag

                        # viterbi algorithm with one-count smoothing
                        p_one_smooth = prob_tt(current_tag, prev_tag) + prob_wt(current_tag, words[i])
                        new_mu2 = mu2[prev_tag][i-1] + p_one_smooth
                        if new_mu2 > mu2[current_tag][i]:
                                mu2[current_tag][i] = new_mu2
                                backpointer2[i] = prev_tag

# check accuracy
def calc_accuracy (backpointer):
        comparisons = 0
        total_matches = 0
        known_comparisons = 0
        known_matches = 0
        unknown_comparisons = 0
        unknown_matches = 0
        novel_comparisons = 1

        backpointer = backpointer[1:]

        i = 0
        unique_words = []
        for a,s in zip(backpointer[1:], tags):
                comparisons += 1
                if words[i] in word_tag_counts.keys():
                        # known
                        known_comparisons += 1
                        if backpointer[i] == tags[i]:
                                known_matches += 1
                                total_matches += 1
                else:
                        # unknown
                        unknown_comparisons += 1 
                        if words[i] not in unique_words:
                                unique_words.append(words[i])
                        if backpointer[i] == tags[i]:
                                unknown_matches += 1
                                total_matches += 1
                i += 1

        if len(unique_words) > 0:
                novel_comparisons += len(unique_words)
        else:
                novel_comparisons = unknown_comparisons

        if novel_comparisons == 0:
                novel_comparisons = 1

        print('Tagging accuracy (Viterbi decoding): ', (total_matches/comparisons)*100, 
                '% (known: ', (known_matches/known_comparisons)*100, 
                '% novel: ', (unknown_matches/novel_comparisons)*100, '%)\n')

print('original viterbi accuracy')
calc_accuracy(backpointer)
print('\nviterbi with one-count smoothing accuracy')
calc_accuracy(backpointer2)
