from typing import Tuple, List

from _utils import read_input, sign, timer

from collections import defaultdict


def process_input(line: str) -> Tuple[List[int], List[int]]:
    """
    Returns a tuple of x,y coordinates from a line of the input.

    Ex:
        process_input("0,9 -> 5,9")
        > ([0,9], [5,9])
    """
    coords1, coords2 = line.split(" -> ")
    coords1 = [int(i) for i in coords1.split(",")]
    coords2 = [int(i) for i in coords2.split(",")]
    return coords1, coords2


def turn_lines_to_points(line):
    """
    Return all the points on the segment between an end and start points, including the latter.
    Handles vertical, horizontal, and diagonal (45 degree) lines.
    """
    coords1, coords2 = line
    x1, y1 = coords1
    x2, y2 = coords2

    abs_dist = max(abs(x2 - x1), abs(y2 - y1))
    x_dir = sign(x2 - x1)
    y_dir = sign(y2 - y1)
    return ((x1 + r * x_dir, y1 + r * y_dir) for r in range(abs_dist + 1))


def count_overlapping_lines(_input: list) -> int:
    """
    Returns the number of points that have 2 segments
    going through them or more.
    """
    counter = defaultdict(int)
    for line in _input:
        points_list = turn_lines_to_points(line)
        for point in points_list:
            counter[point] += 1

    filtered_points = [k for k, v in counter.items() if v >= 2]
    return len(filtered_points)


@timer
def main(filepath: str) -> Tuple[int, int]:
    """
    Returns solution for AOC day 5 from input filepath.
    """
    _input = read_input(filepath)
    _input = [process_input(line) for line in _input]

    part_1_input = [
        line for line in _input if line[0][0] == line[1][0] or line[0][1] == line[1][1]
    ]
    part_1_score = count_overlapping_lines(part_1_input)
    part_2_score = count_overlapping_lines(_input)

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc5.txt")
    print(f"PART 1: {part_1_score}")  # 6710
    print(f"PART 2: {part_2_score}")  # 20121
