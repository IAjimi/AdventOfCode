import itertools

def part1_solution1(_input):
    solution = [i for i in _input if 2020 - i in _input]
    return solution[0] * solution[1]

def part1_solution2(_input):
    matching_input = [2020 - i for i in _input]
    _input, matching_input = set(_input), set(matching_input)
    solution = list(_input.intersection(matching_input))
    return solution[0] * solution[1]

def part2_solution(_input):
    all_combinations = list(itertools.combinations(_input, 3))
    solution = [(i[0], i[1], i[2]) for i in all_combinations if sum(i) == 2020][0]
    return solution[0] * solution[1] * solution[2]

if __name__ == "__main__":
    _input = open("aoc_1.txt").read().splitlines()
    _input = [int(i) for i in _input]
    
    print("PART 1")
    part1_solution1(_input)
    print("")
    print("PART 2")
    part2_solution(_input)