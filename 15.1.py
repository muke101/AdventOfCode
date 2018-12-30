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


def lookUp(x,y):
	return rawMap[graphedMap[y][x]-1]

def graphNeighbors(coords, target):
	x,y = coords
	return filter(lambda coords: lookUp(coords[0],coords[1]) not in ('#', ['E' if target == 'G' else 'G']), [(x+1,y),(x,y+1),(x-1,y),(x,y-1)])

def distance(target, paths):
	current = target
	path = []
	while current != None:
		path.append(current)
		current = paths[current]
	return path

def breadthSearch(xStart, yStart, target): #returns the shortest path by read order to next enemy
	cameFrom = {}
	targets = []
	cameFrom[(xStart,yStart)] = None
	frontier = collections.deque()
	frontier.append((xStart,yStart))

	while len(frontier) != 0:
		current = frontier.popleft()
		for x,y in graphNeighbors(current, target):
			if (x,y) not in cameFrom:
				cameFrom[(x,y)] = current
				if lookUp(x,y) == target:
					targets.append((x,y))
				else: 
					frontier.append((x,y))

	if len(targets) == 0:
		return 1

	#finding distances to all detected targets, handles paths of equal length
	paths = []
	distances = {}
	matches = collections.defaultdict(list)
	for targ in targets:
		paths.append(distance(targ, cameFrom))
	for c, path in enumerate(paths):
		length = len(path)
		if length in distances.values():
			matches[length].append(path)
		distances[c] = length
	minimum = min(paths, key=len)
	if len(minimum) in matches:
		return min(matches[len(minimum)])[1:-1] #smallest x and y values will equate to read order
	else:
		return minimum[1:-1] #cut off start (-1) and target (1)

def attack(x,y,target):
	targets = []
	matches = collections.defaultdict(list)
	choices = {}
	for x,y in graphNeighbors((x,y),target):
		if lookUp(x,y) == target:
			targets.append((x,y))
	for c, i in enumerate(targets):
		targetsHealth = health[i]
		if targetsHealth in choices:
			matches[targetsHealth].append(i)
		choices[c] = targetsHealth
	chosenHealth = min(choices)
	if chosenHealth in matches:
		chosen = min(matches[choices[chosenHealth]]) #jesus fucking christ I have to be doing something avoidable here
	else:
		chosen = targets[chosenHealth]
	health[chosen]-=3
	#print(health)
	if health[chosen] <= 0:
		rawMap[graphedMap[chosen[1]][chosen[0]]-1] = '.'
		del health[chosen]
		del moved[chosen]

health = {}
moved = {}

for y in range(yLen):
	for x in range(xLen):
		if lookUp(x,y) in ('E', 'G'):
			health[(x,y)] = 200
			moved[(x,y)] = False

rounds = 0
breaking = False
while len([i for i in rawMap if i == 'E']) != 0 and len([i for i in rawMap if i == 'G']) != 0:
	moved = dict.fromkeys(moved, False)
	print([i for i in rawMap if i == 'G'])
	for y in range(yLen):
		for x in range(xLen):
			if lookUp(x,y) == 'E' and moved[(x,y)] == False:
				path = breadthSearch(x,y,'G')
				if path != 1: #TODO: elves/goblins won't move if they're blocked for a turn, kinda dumb
					if len(path) == 0: #if next to target
						attack(x,y,'G')
					else:
						xNew,yNew = path[-1]
						rawMap[graphedMap[y][x]-1] = '.'
						rawMap[graphedMap[yNew][xNew]-1] = 'E'
						moved[(x,y)] = True
						moved[(xNew,yNew)] = moved.pop((x,y))
						health[(xNew,yNew)] = health.pop((x,y))
						if len(path) == 1: #ignore the already moved coordinate so don't have to recalculate
							attack(xNew,yNew,'G')
			if lookUp(x,y) == 'G' and moved[(x,y)] == False:
				path = breadthSearch(x,y,'E')
				if path != 1:
					if len(path) == 0:
						attack(x,y,'E')
					else:
						xNew,yNew = path[-1]
						rawMap[graphedMap[y][x]-1] = '.'
						rawMap[graphedMap[yNew][xNew]-1] = 'G'
						moved[(x,y)] = True
						moved[(xNew,yNew)] = moved.pop((x,y))
						health[(xNew,yNew)] = health.pop((x,y))
						if len(path) == 1:
							attack(xNew,yNew,'E')
	rounds+=1

totalHealth = 0
for y in range(yLen):
	for x in range(xLen):
		if lookUp(x,y) in ('E', 'G'):
			totalHealth+=health[(x,y)]

print(rounds, totalHealth)
print(totalHealth*rounds)