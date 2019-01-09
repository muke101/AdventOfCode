import sys

strings = sys.stdin.read().splitlines()

double = 0
tripple = 0
broken = False
for string in strings:
	for i in strings:
		diffnces = [(i,j) for i,j in zip(string, i) if i != j]
		if len(diffnces) == 1 and string.index(diffnces[0][0]) == i.index(diffnces[0][1]):
			andset = list(set(string)&set(i))
			print(''.join([i for i in string if i in andset]))
			broken = True
			break
	if broken == True:
		break

