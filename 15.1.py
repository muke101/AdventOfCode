import sys
import numpy as np
import collections

rawMap = sys.stdin.read() #piping in map via cat
xLen = 0
for i in rawMap:
	if i != '\n':
		xLen+=1
	else:
		break
yLen = len([i for i in rawMap.splitlines()])

rawMap = list(rawMap.replace('\n', ''))
graphedMap = np.empty((yLen, xLen), dtype=int)
iterator = enumerate(rawMap, start=1)
for y in range(yLen):
	for x in range(xLen):
		graphedMap[y][x] = next(iterator)[0]

def lookUp(y,x):
	return rawMap[graphedMap[y][x]-1]

def graphNeighbors(coords, target):
	y,x = coords
	return filter(lambda coords: lookUp(coords[0],coords[1]) not in ('#', ['E' if target == 'G' else 'G'][0]), [(y,x+1),(y+1,x),(y,x-1),(y-1,x)])

def distance(target, paths):
	current = target
	path = []
	while current != None:
		path.append(current)
		current = paths[current]
	return path

def breadthSearch(yStart, xStart, target): #returns the shortest path by read order to next enemy
	cameFrom = {}
	targets = []
	cameFrom[(yStart,xStart)] = None
	frontier = collections.deque()
	frontier.append((yStart,xStart))

	while len(frontier) != 0:
		current = frontier.popleft()
		for y,x in graphNeighbors(current, target):
			if (y,x) not in cameFrom:
				cameFrom[(y,x)] = current
				if lookUp(y,x) == target:
					targets.append((y,x))
				else: 
					frontier.append((y,x))

	if len(targets) == 0:
		return 1

	#finding distances to all detected targets, handles paths of equal length
	paths = []
	distances = set()
	matches = collections.defaultdict(list)
	for targ in targets:
		paths.append(distance(targ, cameFrom))
	for path in paths:
		matches[len(path)].append(path)
	minimum = min(paths, key=len)
	return min(matches[len(minimum)])[1:-1] #smallest x and y values will equate to read order, [1:-1] to cut off start and end destinations

def attack(y,x,target):
	targets = []
	matches = collections.defaultdict(list)
	choices = set()
	for y,x in graphNeighbors((y,x),target):
		if lookUp(y,x) == target:
			targets.append((y,x))
	for targ in targets:
		targetsHealth = health[targ]
		matches[targetsHealth].append(targ)
		choices.add(targetsHealth)
	chosenHealth = min(choices)
	chosen = min(matches[chosenHealth])

	health[chosen]-=3
	if health[chosen] <= 0:
		rawMap[graphedMap[chosen[0]][chosen[1]]-1] = '.'
		del health[chosen]
		del moved[chosen]
		return 0
	return 1

def move(y,x,yNew,xNew,path,target):
	rawMap[graphedMap[y][x]-1] = '.'
	rawMap[graphedMap[yNew][xNew]-1] = ['E' if target == 'G' else 'G'][0]
	moved[(y,x)] = True
	moved[(yNew,xNew)] = moved.pop((y,x))
	health[(yNew,xNew)] = health.pop((y,x))

health = {}
moved = {}

for y in range(yLen):
	for x in range(xLen):
		if lookUp(y,x) in ('E', 'G'):
			health[(y,x)] = 200
			moved[(y,x)] = False

rounds = 0
breaking = False
while len([i for i in rawMap if i == 'E']) != 0 and len([i for i in rawMap if i == 'G']) != 0:
	print(''.join(np.insert(rawMap, [i*xLen for i in range(1,yLen)], '\n')), '\n')
	moved = dict.fromkeys(moved, False)
	for y in range(yLen):
		for x in range(xLen): #TODO: if a unit is blocked by another unit, which then dies after the original unit has been parsed, must go back to that unit and carry out it's turn
			if lookUp(y,x) == 'E' and moved[(y,x)] == False: #does this mean that units blocked by then dead units should recalculate their turns? Fuck. 
				path = breadthSearch(y,x,'G')
				if path != 1: #returns 1 if no targets found
					if len(path) == 0: #if next to target
						if attack(y,x,'G') == 0: #returns 0 if target killed
							path = breadthSearch(y,x,'G')
							if path != 1 and len(path) != 0:
								yNew,xNew = path[-1]
								move(y,x,yNew,xNew,path,'G')
					else:
						yNew,xNew = path[-1]
						move(y,x,yNew,xNew,path,'G')
						if len(path) == 1: #ignore the already moved coordinate so don't have to recalculate
							attack(yNew,xNew,'G')

			if lookUp(y,x) == 'G' and moved[(y,x)] == False:
				path = breadthSearch(y,x,'E')
				if path != 1:
					if len(path) == 0:
						if attack(y,x,'E') == 0:
							path = breadthSearch(y,x,'E')
							if path != 1 and len(path) != 0:
								yNew,xNew = path[-1]
								move(y,x,yNew,xNew,path,'E')
					else:
						yNew,xNew = path[-1]
						move(y,x,yNew,xNew,path,'E')
						if len(path) == 1:
							attack(yNew,xNew,'E')
	rounds+=1
rounds-=1

totalHealth = 0
for y in range(yLen):
	for x in range(xLen):
		if lookUp(y,x) in ('E', 'G'):
			totalHealth+=health[(y,x)]
print(''.join(np.insert(rawMap, [i*xLen for i in range(1,yLen)], '\n')), '\n')
print(rounds, totalHealth)
print(totalHealth*rounds)