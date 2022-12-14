from typing import Tuple

from _utils import read_input, timer, Solution, GridDict

SAND = 0
ROCK = 1

SAND_START_X, SAND_START_Y = 500, 0


def process_input(filename: str) -> GridDict:
    _input = read_input(filename)

    grid = {}

    for path in _input:
        rocks = path.split(" -> ")
        for i in range(len(rocks) - 1):
            r1, r2 = rocks[i], rocks[i + 1]
            x1, y1 = map(int, r1.split(","))
            x2, y2 = map(int, r2.split(","))

            if x1 == x2:
                min_y, max_y = min(y1, y2), max(y1, y2)
                for y in range(min_y, max_y + 1):
                    grid[(x1, y)] = ROCK
            elif y1 == y2:
                min_x, max_x = min(x1, x2), max(x1, x2)
                for x in range(min_x, max_x + 1):
                    grid[(x, y1)] = ROCK
            else:
                raise Exception

    return grid


def pour_sand(grid: GridDict, x: int, y: int, max_y: int) -> Tuple[int, int, bool]:
    while y < max_y:
        if (x, y + 1) not in grid:  # falls down one step
            y += 1
        elif (x - 1, y + 1) not in grid:  # one step down and to the left
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in grid:  # one step down and to the right
            x += 1
            y += 1
        else:
            return x, y, True

    return x, y, False


def part_1_simulation(grid: GridDict) -> int:
    max_y = max({k[1] for k in grid})

    while True:
        x, y, at_rest = pour_sand(grid, SAND_START_X, SAND_START_Y, max_y)
        if at_rest:
            grid[(x, y)] = SAND
        else:
            return len({k for k, v in grid.items() if v == SAND})


def part_2_simulation(grid: GridDict) -> int:
    max_y = max({k[1] for k in grid}) + 2

    # add bottom line
    max_x = max({k[0] for k in grid})
    for x in range(0, max_x + 200):
        grid[(x, max_y)] = ROCK

    while True:
        x, y, at_rest = pour_sand(grid, SAND_START_X, SAND_START_Y, max_y)
        grid[(x, y)] = SAND
        if (x, y) == (SAND_START_X, SAND_START_Y):
            return len({k for k, v in grid.items() if v == SAND})


@timer
def main(filename: str) -> Solution:
    grid = process_input(filename)
    part_1_solution = part_1_simulation(grid.copy())
    part_2_solution = part_2_simulation(grid.copy())
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc14.txt")
    print(f"PART 1: {part_1_solution}")  # 1072
    print(f"PART 2: {part_2_solution}")  # 24659
