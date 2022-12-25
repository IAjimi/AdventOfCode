from typing import List

from _utils import read_input, timer, Solution


def process_input(_input: List[str]) -> List[int]:
    inventory = [0]

    for line in _input:
        if line == "":
            inventory.append(0)
        else:
            inventory[-1] += int(line)

    inventory.sort()
    return inventory


@timer
def main(filename: str) -> Solution:
    _input = read_input(filename)
    calories = process_input(_input)
    part_1_solution = calories[-1]
    part_2_solution = sum(calories[-3:])
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc1.txt")
    print(f"PART 1: {part_1_solution}")  # 74394
    print(f"PART 2: {part_2_solution}")  # 212836
