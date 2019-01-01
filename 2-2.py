import sys

strings = sys.stdin.read().splitlines()

double = 0
tripple = 0
broken = False
for string in strings:
	for i in strings:
		xor = list(set(string)^set(i))
		if len(xor) == 2:
			if xor[0] in string and string.index(xor[0]) == i.index(xor[1]):
				andset = list(set(string)&set(i))
				print(''.join(andset))
				print(''.join([i for i in string if i in andset]))
				broken = True
				break
			elif xor[1] in string and string.index(xor[1]) == i.index(xor[0]):
				andset = set(string)&set(i)
				print(string,i)
				print(''.join(andset))
				print(''.join([i for i in string if i in andset]))
				broken = True
				break
	if broken == True:
		break

