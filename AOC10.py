''' Only part 1. '''

import numpy as np
from collections import Counter

def chain_adapters(_input):
    l = _input
    l.sort()

    shift_l = [0] + l[:-1]
    l, shift_l = np.array(l), np.array(shift_l)

    solution = list(l - shift_l) + [3]
    solution = Counter(solution)
    return solution[1] * solution[3]

def find_valid_arrangements(_input):
    ''' Not my answer, trying to get dynamic programming
    found at https://dev.to/rpalo/advent-of-code-2020-solution-megathread-day-10-adapter-array-33ea'''
    adapters = _input
    adapters.sort()
    adapters = [0] + adapters
    valid_arrangements = [1] * len(adapters) # cumulative sum of valid paths 

    for index in range(1, len(adapters)):
        valid_arrangements[index] = sum(
            valid_arrangements[src_index]
            for src_index in range(max(0, index - 3), index) # prev 3 values to this value
            if adapters[index] - adapters[src_index] <= 3 # if distance is within range
        )
    print(valid_arrangements[-1])

if __name__ == "__main__":
    _input = open("aoc_10.txt").read().splitlines()
    _input = [int(i) for i in _input]
    
    print("PART 1")
    chain_adapters(_input)
    print("")
    print("PART 2")

