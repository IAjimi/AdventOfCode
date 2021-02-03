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

def create_path_dict(_input):
    travel_dict = {}

    for i in _input:
        dest = []

        if i + 1 in _input:
            dest.append(i + 1)
        if i + 2 in _input:
            dest.append(i + 2)
        if i + 3 in _input:
            dest.append(i + 3)

        travel_dict[i] = dest

    return travel_dict

def find_n_paths(graph, start, end, path=[], n = 0):
    '''In progress, adapted graph traversal function from somewhere online.'''
    path = path + [start]
    if start == end:
        n += 1
        return n
    if start not in graph.keys():
        return None
    for node in graph[start]:
        if node not in path:
            n = find_n_paths(graph, node, end, path, n)
    return n

def find_n_paths(_input):
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

