from typing import List, Set, Tuple

from _utils import read_input, timer, Point


def parse_input(_input: List[str]) -> Tuple[Set[Point], List[str]]:
    grid = set()
    instructions = []

    for line in _input:
        if "," in line:
            x, y = line.split(",")
            grid.add((int(x), int(y)))
        elif "fold along" in line:
            instructions.append(line)

    return grid, instructions


def vertical_flip(grid: Set[Point], flip_val: int) -> Set[Point]:
    new_grid = set()
    for x, y in grid:
        if y > flip_val:
            new_y = 2 * flip_val - y
            new_grid.add((x, new_y))
        else:
            new_grid.add((x, y))
    return new_grid


def horizontal_flip(grid: Set[Point], flip_val: int) -> Set[Point]:
    new_grid = set()
    for x, y in grid:
        if x > flip_val:
            new_x = 2 * flip_val - x
            new_grid.add((new_x, y))
        else:
            new_grid.add((x, y))
    return new_grid


def print_grid(grid: Set[Point]) -> str:
    grid_str = ""
    max_x = 1 + max((pos[0] for pos in grid))
    max_y = 1 + max((pos[1] for pos in grid))

    for y in range(max_y):
        line = ["#" if (x, y) in grid else "." for x in range(max_x)]
        grid_str += " ".join(line)
        grid_str += "\n"

    return grid_str


@timer
def main(filepath: str) -> Tuple[int, Set[Point]]:
    _input = read_input(filepath)
    grid, instructions = parse_input(_input)

    for ix, instr in enumerate(instructions):
        _, flip_val = instr.split("=")
        flip_val = int(flip_val)

        if "x" in instr:
            grid = horizontal_flip(grid, flip_val)
        elif "y" in instr:
            grid = vertical_flip(grid, flip_val)

        if ix == 0:
            part_1_score = len(grid)

    return part_1_score, grid


if __name__ == "__main__":
    part_1_score, part_2_grid = main("aoc13.txt")
    print(f"PART 1: {part_1_score}")  # 850
    print(f"PART 2: \n {print_grid(part_2_grid)}")  # AHGCPGAU
