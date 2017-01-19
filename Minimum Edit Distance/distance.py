'''
distance.py

Minimum Edit Distance
CSCI 404 - Natural Language Processing
Authors: Raymond Weiming Luo and Ben Ellerby

'''

def backtrace (dist, target, source, tAlign, sAlign, opAlign, stack):
	print "STACK: ", stack, "\n"

	if not stack:
		print tAlign, "\n", opAlign, "\n", sAlign, "\n"
		return

	coordinates = stack.pop()

	if dist[coordinates[0]-1][coordinates[1]] == 0:
		print tAlign, "\n", opAlign, "\n", sAlign, "\n"

	if dist[coordinates[0]][coordinates[1]-1] == 0:
		print tAlign, "\n", opAlign, "\n", sAlign, "\n"

	if dist[coordinates[0]][coordinates[1]] == 0:
		print tAlign, "\n", opAlign, "\n", sAlign, "\n"

        node = dist[coordinates[0]][coordinates[1]]
	
	# Check left
	if (coordinates[0]-1 >= 0 and (dist[coordinates[0]-1][coordinates[1]]+1) == node):
		#tAlign = target[coordinates[0]-1] + " " + tAlign
		#sAlign = "_ " + sAlign
		#opAlign = "  " + opAlign
		stack.append([coordinates[0]-1, coordinates[1]])
		op = "i"

	# Check up
	if (coordinates[1]-1 >= 0 and (dist[coordinates[0]][coordinates[1]-1]+1) == node):
		#tAlign = "_ " + tAlign
		#sAlign = source[coordinates[1]-1] + " " + sAlign
		#opAlign = "  " + opAlign
		stack.append([coordinates[0], coordinates[1]-1])
		op = "d"

	# Check diagonal
	if (coordinates[0]-1 >= 0 and coordinates[1]-1 >= 0 and (dist[coordinates[0]-1][coordinates[1]-1]) == node):
		#tAlign = target[coordinates[0]-1] + " " + tAlign
		#sAlign = source[coordinates[1]-1] + " " + sAlign
		#opAlign = "| " + opAlign
		stack.append([coordinates[0]-1, coordinates[1]-1])
		op = "|"
	
	if (coordinates[0]-1 >= 0 and coordinates[1]-1 >= 0 and (dist[coordinates[0]-1][coordinates[1]-1]+2) == node):
		#tAlign = target[coordinates[0]-1] + " " + tAlign
		#sAlign = source[coordinates[1]-1] + " " + sAlign
		#opAlign = "  " + opAlign
		stack.append([coordinates[0]-1, coordinates[1]-1])
		op = "s"

	backtrace(dist, target, source, tAlign, sAlign, opAlign, stack, op)

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

	print 'levenshtein distance =', dist[n-1][m-1], '\n'
	return dist

if __name__=="__main__":
	from sys import argv
	alignments = 100
	stack = []
	
	if (len(argv) > 2):
		if (len(argv) == 4):
			alignments = argv[3]
                
		dist = distance(argv[1], argv[2], 1, 1, 2)
		print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in dist]))		

		stack.append([len(argv[1]), len(argv[2])])
		backtrace(dist, argv[1], argv[2], "", "", "", stack)
	else:
		print 'ERROR: Not enough arguments.\n'
