from collections import Counter

def computeChecksum(_input):
	two_match = 0
	three_match = 0

	for word in _input:
	    _count = dict(Counter(word))
	    
	    if 2 in _count.values(): two_match += 1
	    if 3 in _count.values(): three_match += 1

	return two_match * three_match

def computeDifference(string1, string2):
	'''Returns -1 if there is more than 1 different
	character between the two strings and 1 if <= 1.'''
    _count = 0
    
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            _count += 1
        if _count > 1:
            return -1
        
    return 1

def findMinDiff(_input):
	n = len(_input)

	for i in range(n):
    	for j in range(i):
        	if i != j:
            	num = computeDifference(_input[i], _input[j])
            	if num == 1: return _input[i], _input[j]

if __name__ == "__main__":
    _input = open("aoc_2.txt").read().splitlines()

    print("PART 1")
    print(computeChecksum(_input)) # 4940
    print("PART 2")
    print(findMinDiff(_input)) # wrziyfdmlumeqvaatbiosngkc