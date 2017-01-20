'''
distance.py

Minimum Edit Distance
CSCI 404 - Natural Language Processing
Authors: Raymond Weiming Luo and Ben Ellerby

'''

count = 0

def backtrace (target, source, tAlign, sAlign, opAlign, dist, fdist, node, op):
	x = node[0]
	y = node[1]

	cost = dist[x][y]

	fdist[x][y] = -1
	
	'''
	print '-------------------------------------------'
	#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in dist])), "\n"
	print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in fdist])), "\n"
	print node
	'''

	if (op is 'i'):
		tAlign = target[x] + ' ' + tAlign
		sAlign = '_ ' + sAlign
		opAlign = '  ' + opAlign
	elif (op is 'd'):
		tAlign = '_ ' + tAlign
		sAlign = source[y] + ' ' + sAlign
		opAlign = '  ' + opAlign
	elif (op is '|'):
		tAlign = target[x] + ' ' + tAlign
		sAlign = source[y] + ' ' + sAlign
		opAlign = '| ' + opAlign
	elif (op is 's'):
		tAlign = target[x] + ' ' + tAlign
		sAlign = source[y] + ' ' + sAlign
		opAlign = '  ' + opAlign

	if (x == 0 and y == 0):
		global count
		count = count + 1
		print tAlign, '\n', opAlign, '\n', sAlign, '\n'
		print '-------------------------------------------\n'
	else:
		if (fdist[x-1][y] != -1 and dist[x-1][y]+1 == cost):
			backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y], 'i')
		if (fdist[x][y-1] != -1 and dist[x][y-1]+1 == cost):
			backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x, y-1], 'd')
		if (fdist[x-1][y-1] != -1 and dist[x-1][y-1] == cost and target[x-1] == source[y-1]):
			backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y-1], '|')
		if (fdist[x-1][y-1] != -1 and dist[x-1][y-1]+2 == cost):
			backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y-1], 's')

	fdist[x][y] = dist[x][y]
	#tAlign = tAlign[2:]
	#sAlign = sAlign[2:]
	#opAlign = opAlign[2:]

def distance (target, source, insertcost, deletecost, replacecost):
	n = len(target)+1
	m = len(source)+1

    # set up dist and initialize valuesi
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

	print 'levenshtein distance =', dist[n-1][m-1], '\n'
	return dist

if __name__=="__main__":
	from sys import argv
	global count
	alignments = 100
	
	if (len(argv) > 2):
		if (len(argv) == 4):
			alignments = argv[3]
                
		dist = distance(argv[1], argv[2], 1, 1, 2)
		fdist = [row[:] for row in dist]
		#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in dist]))
		backtrace(argv[1], argv[2], '', '', '', dist, fdist, [len(argv[1]), len(argv[2])], '')
		#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in dist]))
		print "COUNT: ", count
	else:
		print 'ERROR: Not enough arguments.\n'
