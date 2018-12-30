import csv

puzzleInput = csv.reader(open('input/1-1.csv'), delimiter='\n')
freq = 0
for line in puzzleInput:
	number = int(line[0][1:])
	freq += [number*-1 if line[0][:1] == '-' else number][0]
print(freq)