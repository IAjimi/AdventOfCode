from typing import Tuple

from _utils import read_input, timer, Solution


def parse_line(line: str) -> Tuple[int, int, int, int]:
    elf1, elf2 = line.split(",")
    x1, x2 = list(map(int, elf1.split("-")))
    y1, y2 = list(map(int, elf2.split("-")))
    return x1, x2, y1, y2


def process_input(filepath: str) -> Solution:
    _input = read_input(filepath)

    fully_contained = 0
    overlap = 0

    for line in _input:
        x1, x2, y1, y2 = parse_line(line)

        if (x1 <= y1 <= y2 <= x2) or (y1 <= x1 <= x2 <= y2):
            fully_contained += 1
            overlap += 1
        elif (x1 <= y1 <= x2) or (y1 <= x1 <= y2):
            overlap += 1

    return fully_contained, overlap


@timer
def main(filename: str) -> Solution:
    fully_contained, overlap = process_input(filename)
    part_1_solution = fully_contained
    part_2_solution = overlap
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc4.txt")
    print(f"PART 1: {part_1_solution}")  # 448
    print(f"PART 2: {part_2_solution}")  # 794
