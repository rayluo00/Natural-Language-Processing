'''
distance.py

Minimum Edit Distance Algorithm
CSCI 404 - Natural Language Processing
Last Modified By: Raymond Weiming Luo and Ben Ellerby

'''

def backtrace (dist, i, j, target, source):
	mincost = dist[i][j]

	if (mincost == dist[i-1][j-1] and source[j-1] == target[i-1]):
		return (i-1), (j-1), '|'
	if (mincost == dist[i-1][j-1]+2):
		return (i-1), (j-1), ' '
	if (mincost == dist[i-1][j]+1):
		return (i-1), j, 'i'
	if (mincost == dist[i][j-1]+1):
		return i, (j-1), 'd'


def distance (target, source, insertcost, deletecost, replacecost):
	n = len(target)+1
	m = len(source)+1

    # set up dist and initialize values
	dist = [ [0 for j in range(m)] for i in range(n) ]
	for i in range(1,n):
		dist[i][0] = dist[i-1][0] + insertcost
	for j in range(1,m):
		dist[0][j] = dist[0][j-1] + deletecost

    # align source and target strings
	for j in range(1,m):
		for i in range(1,n):
			inscost = insertcost + dist[i-1][j]
			delcost = deletecost + dist[i][j-1]

			if (source[j-1] == target[i-1]):
				add = 0
			else: 
				add = replacecost

			substcost = add + dist[i-1][j-1]
			dist[i][j] = min(inscost, delcost, substcost)

	print "\n"
	i = n - 1
	j = m - 1
	while (i > 0 or j > 0):
		i2, j2, op = backtrace(dist, i, j, target, source)
		
		if (op == 'i'):
			print target[i-1], "  _"
		elif (op == 'd'):
			print "_  ", source[j-1]
		else:
			print target[i-1], op, source[j-1]
		i = i2
		j = j2
	print "\n"	

	# return min edit distance
	return dist[n-1][m-1]

if __name__=="__main__":
    from sys import argv
    if len(argv) > 2:
        print "levenshtein distance =", distance(argv[1], argv[2], 1, 1, 2)
