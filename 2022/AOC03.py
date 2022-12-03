from collections import defaultdict
from typing import List, Tuple

from _utils import read_input, timer


def get_score(char):
    if char.islower():
        return 1 + ord(char) - ord("a")
    else:
        return 27 + ord(char) - ord("A")


def part_1(_input):

    total = 0
    for rucksack in _input:
        first_half_index = len(rucksack) // 2
        first_half_set = {c for c in rucksack[:first_half_index]}

        for char in rucksack[first_half_index:]:
            if char in first_half_set:
                total += get_score(char)
                break  # only 1 dupe per rucksack, can appear multiple times in 2nd half
    return total


def part_2(_input):
    total = 0

    for group_id in range(0, len(_input), 3):
        group_sack = defaultdict(int)

        for rucksack in _input[group_id : group_id + 3]:
            unique_items = {c for c in rucksack}
            for char in unique_items:
                group_sack[char] += 1

        dupe = {
            char for char, n in group_sack.items() if n == 3
        }  # dupe is in all 3 rucksacks
        total += sum({get_score(c) for c in dupe})
    return total


@timer
def main(filename: str) -> Tuple[int, int]:
    _input = read_input(filename)
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc3.txt")
    print(f"PART 1: {part_1_score}")  # 7824
    print(f"PART 2: {part_2_score}")  # 2798
