def find_repeated_freq(_input):
	_sum = 0
	found = False
	frequencies = [0]

	while not found:
	    for i in _input:
	        _sum += i
	        
	        if _sum in frequencies:
	            return _sum
	        else:
	            frequencies.append(_sum)

if __name__ == "__main__":
    _input = open("aoc_1.txt").read().splitlines()
    _input = [int(i) for i in _input]

    print("PART 1")
    print(sum(_input)) # 477
    print("PART 2")
    print(find_repeated_freq(_input)) # 390, slow bc brute force