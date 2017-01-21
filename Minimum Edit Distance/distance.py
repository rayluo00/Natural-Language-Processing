'''
distance.py

Minimum Edit Distance
CSCI 404 - Natural Language Processing
Authors: Raymond Weiming Luo and Ben Ellerby

This program computes the minimum levenshtein distance when comparing
two strings using dynamic programming. The minimum levenshtein distance
is calculated using a 2d matrix to find the minimum edits. The result is 
located on position (n-1, m-1), where n is the length of the target and 
m is the length of the source. The output displays the various alignments
of the levenshtein distance. A third argument is optional to display the 
number of alignments, otherwise the default display is 100 alignments.

'''

count = 0

#######################################################################################
'''
Perform a recursive DFS search on the 2d matrix that was generated when computing
the levenshtein distance. Create three strings to display the target, source and 
operations used for the alignment. If a third argument was passed to the main
function, display a total of the input number's alignments. Otherwise, the default
alignment print count is 100 alignments.
'''
def backtrace (target, source, tAlign, sAlign, opAlign, dist, fdist, node, op, alignments):
	global count

	#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in fdist])), "\n"

	if count >= alignments:
		return
	else:
		x = node[0]
		y = node[1]

		cost = dist[x][y]

		fdist[x][y] = -1

		# Format the alignment string for a specified operation.
		if (op is 'i'):
			tAlign = target[x] + ' ' + tAlign
			sAlign = '_ ' + sAlign
			opAlign = '  ' + opAlign
		elif (op is 'd'):
			tAlign = '_ ' + tAlign
			sAlign = source[y] + ' ' + sAlign
			opAlign = '  ' + opAlign
		elif (op is '|' or op is 's'):
			tAlign = target[x] + ' ' + tAlign
			sAlign = source[y] + ' ' + sAlign
			
			if (op is '|'):
				opAlign = '| ' + opAlign
			elif (op is 's'):
				opAlign = '  ' + opAlign

		# If position is at (0,0), we have concluded a possible alignment.
		# Else, do a recursive DFS search to find possible alignments.
		if (x == 0 and y == 0):
			count = count + 1
			print tAlign, '\n', opAlign, '\n', sAlign, '\n'
			print '----------------------',count,'---------------------\n'
		else:
			if (fdist[x-1][y] != -1 and dist[x-1][y]+1 == cost):
				backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y], 'i', alignments)
			if (fdist[x][y-1] != -1 and dist[x][y-1]+1 == cost):
				backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x, y-1], 'd', alignments)
			if (fdist[x-1][y-1] != -1 and dist[x-1][y-1] == cost and target[x-1] == source[y-1]):
				backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y-1], '|', alignments)
			if (fdist[x-1][y-1] != -1 and dist[x-1][y-1]+2 == cost):
				backtrace(target, source, tAlign, sAlign, opAlign, dist, fdist, [x-1, y-1], 's', alignments)

		fdist[x][y] = cost

#######################################################################################
'''
Calculate the levenshtein distance by comparing two strings by using dynamic
programming. A 2d matrix is used to find the minimum levenshtein distance at
position (n-1, m-1) where n = length of string 1 and m = length of string 2.
'''
def distance (target, source, insertcost, deletecost, replacecost):
	n = len(target)+1
	m = len(source)+1

    # Set up dist and initialize values
	dist = [ [0 for j in range(m)] for i in range(n) ]
	for i in range(1,n):
		dist[i][0] = dist[i-1][0] + insertcost
	for j in range(1,m):
		dist[0][j] = dist[0][j-1] + deletecost

    # Align source and target strings
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
	alignments = 100
	
	if (len(argv) > 2):
		if (len(argv) == 4):
			alignments = int(argv[3])
                
		dist = distance(argv[1], argv[2], 1, 1, 2)
		fdist = [row[:] for row in dist]

		backtrace(argv[1], argv[2], '', '', '', dist, fdist, [len(argv[1]), len(argv[2])], '', alignments)
	else:
		print 'ERROR: Not enough arguments.\n'
