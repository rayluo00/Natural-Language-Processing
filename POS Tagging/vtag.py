import nltk

f = open("data/en/entrain.txt").read().split()

l = []
word_tag_counts = {}
tag_counts = {}
cond_tag_counts = {}

for line in f:
	l.append(line.split("/"))

for line in l:
	if line[0] not in word_tag_counts:
		word_tag_counts[line[0]] = {line[1]: 1}
	else:
		if line[1] not in word_tag_counts[line[0]]:
			word_tag_counts[line[0]][line[1]] = 1
		else:
			word_tag_counts[line[0]][line[1]] += 1

for i in range(len(l)):
	current = l[i][1]
	# number of times each tag appears
	if current not in tag_counts:
		tag_counts[current] = 1
	else:
		tag_counts[current] += 1
	# number of times each tag sequence appears
	if i > 0:
		prev = l[i-1][1]
		if current not in cond_tag_counts:
			cond_tag_counts[current] = {prev: 1}
		else:
			if prev not in cond_tag_counts[current]:
				cond_tag_counts[current][prev] = 1
			else:
				cond_tag_counts[current][prev] += 1
	

#print(tag_counts)
#print(cond_tag_counts)
