import sys

strings = sys.stdin.read()

double = 0
tripple = 0
for string in strings.splitlines():
	characters={}
	for character in string:
		if character in characters:
			characters[character]+=1
		else:
			characters[character] = 1
	if 3 in characters.values():
		tripple+=1
	if 2 in characters.values():
		double+=1
print(double*tripple)