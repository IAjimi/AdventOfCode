from typing import Tuple, List

from _utils import read_input, sign, timer, Point, create_grid, get_median

from collections import defaultdict

import parse


def process_input(_input: List[str]) -> List[int]:
    i = 0
    inventory = defaultdict(int)
    for line in _input:
        if line == "":
            i += 1
        else:
            inventory[i] += int(line)

    calories = list(inventory.values())
    calories.sort()
    return calories


@timer
def main(filename: str) -> Tuple[int, int]:
    _input = read_input(filename)
    calories = process_input(_input)
    part_1_score = calories[-1]
    part_2_score = sum(calories[-3:])
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc1.txt")
    print(f"PART 1: {part_1_score}")  # 74394
    print(f"PART 2: {part_2_score}")  # 212836
