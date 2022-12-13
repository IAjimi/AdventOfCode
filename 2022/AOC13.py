from typing import List

from functools import cmp_to_key
from _utils import read_input, timer, Solution, product


def process_input(filename: str) -> List[list]:
    _input = read_input(filename)
    _input = [eval(l) for l in _input if l != ""]
    return _input


def compare_pairs(pair1, pair2) -> int:
    if type(pair1) == int and type(pair2) == int:
        if pair1 < pair2:
            return -1
        elif pair1 > pair2:
            return 1
        else:
            return 0
    elif type(pair1) == list and type(pair2) == int:
        return compare_pairs(pair1, [pair2])
    elif type(pair1) == int and type(pair2) == list:
        return compare_pairs([pair1], pair2)
    else:
        i = 0
        while i < len(pair1) and i < len(pair2):
            p1, p2 = pair1[i], pair2[i]
            comp = compare_pairs(p1, p2)
            if comp != 0:
                return comp
            else:
                i += 1

    if len(pair1) < len(pair2):
        return -1
    elif len(pair1) > len(pair2):
        return 1
    else:
        return 0


def part1(_input) -> int:
    _input = [compare_pairs(_input[i], _input[i + 1]) for i in range(0, len(_input), 2)]
    return sum([1 + i if pair == -1 else 0 for i, pair in enumerate(_input)])


def part2(_input) -> int:
    _input.append([[2]])
    _input.append([[6]])
    _input.sort(key=cmp_to_key(compare_pairs))
    return product([i + 1 for i, v in enumerate(_input) if v in ([[2]], [[6]])])


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    part_1_solution = part1(_input)
    part_2_solution = part2(_input)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc13.txt")
    print(f"PART 1: {part_1_solution}")  # 5185
    print(f"PART 2: {part_2_solution}")  # 23751
