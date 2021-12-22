"""
00:17:00, rank 1326 for part 1.
"""
from typing import Tuple

from _utils import read_input, timer

import parse

Point = Tuple[int, int, int]


def parse_line(line: str) -> Tuple[str, Tuple[int, int, int, int, int, int]]:
    switch_str, x1, x2, y1, y2, z1, z2 = tuple(
        parse.parse("{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line).fixed
    )
    switch_bool = True if switch_str == "on" else False
    return switch_bool, (x1, x2, y1, y2, z1, z2)


def process_reboot_instruction(
    grid: set, switch_bool: bool, coords: Tuple[int, int, int, int, int, int]
) -> set:
    x1, x2, y1, y2, z1, z2 = coords

    if -50 <= x1 <= x2 <= 50 and -50 <= x1 <= x2 <= 50 and -50 <= x1 <= x2 <= 50:
        # cubes = ((x, y, z) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1) for z in range(z1, z2 + 1))
        # print(switch_bool, coords)

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    c = (x, y, z)
                    if switch_bool and c not in grid:
                        grid.add(c)
                    elif not switch_bool and c in grid:
                        grid.remove(c)

    return grid


@timer
def main(filepath: str) -> Tuple[int, int]:
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    _input = [parse_line(line) for line in _input]

    grid = set()
    for switch_bool, coords in _input:
        process_reboot_instruction(grid, switch_bool, coords)

    part_1_score = len(grid)
    part_2_score = 0
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("test_aoc22.txt")
    print(f"PART 1: {part_1_score}")  # 587785
    print(f"PART 2: {part_2_score}")  # .
