import csv

freq = 0
freqs = set()
found = False

while found == False:
	puzzleInput = csv.reader(open('input/1-1.csv'), delimiter='\n')
	for line in puzzleInput:
		if freq in freqs:
			found = True
			print(freq)
			break
		freqs.add(freq)
		number = int(line[0][1:])
		freq += [number*-1 if line[0][:1] == '-' else number][0]