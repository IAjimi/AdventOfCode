import numpy as np
import itertools

def check_sum(_input):
    for i,v in enumerate(_input):
        if i >= 25:
            x = _input[i-25:i]
            all_combinations = list(itertools.combinations(x, 2))
            all_sums = [sum(t) for t in all_combinations]

            if v in all_sums:
                next
            else:
                return v

def find_encryption_weakness(_input, solution):
    '''Logic here is to find contiguous sequence by
    repeatedly adding a rightward-shifted version of
    the sequence to itself. This is like expanding the
    number of contiguous numbers we are considering for 
    the sum by 1 each time.

    n = 1 -> [a, b, c, d, e, ...] + [0, a, b, c, d, ...]
    n = 2 -> [a, a+b, b+c, d+e, ...] + [0, 0, a, b, c, ...]
    n = 3 -> [a, a+b, b+c+d, d+e+f] + [0, 0, 0, a, b, ...]
     '''
    found = False
    l = _input
    n = 0

    while found == False:
        n += 1
        shift_l = [0 for n in range(n)] + _input[:-n]
        l = list(np.array(l) + np.array(shift_l))

        if solution in l:
            found = True
            loc = l.index(solution)
            return _input[loc-n:loc+1]

if __name__ == "__main__":
    _input = open("aoc_9.txt").read().splitlines()
    _input = [int(i) for i in _input]
    
    print("PART 1")
    solution = check_sum(_input)
    print("")
    print("PART 2")
    seq = find_encryption_weakness(_input, solution)
    print(min(seq) + max(seq))
