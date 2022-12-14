from typing import List, Tuple, Set

from _utils import read_input, timer, Solution


def process_input(filename: str):
    _input = read_input(filename)

    grid = {}

    for path in _input:
        rocks = path.split(" -> ")
        for i in range(len(rocks) - 1):
            r1, r2 = rocks[i], rocks[i+1]
            x1, y1 = map(int, r1.split(','))
            x2, y2 = map(int, r2.split(','))

            if x1 == x2:
                min_y, max_y = min(y1, y2), max(y1, y2)
                for y in range(min_y, max_y + 1):
                    grid[(x1, y)] = '#'
            elif y1 == y2:
                min_x, max_x = min(x1, x2), max(x1, x2)
                for x in range(min_x, max_x + 1):
                    grid[(x, y1)] = '#'
            else:
                raise Exception

    return grid

def pour_sand(grid, x, y):
    max_y = max({k[1] for k in grid})

    while True:
        if y > max_y:
            return x, y, False
        elif (x, y+1) not in grid:  # falls down one step
            y += 1
        elif (x-1, y+1) not in grid:  # one step down and to the left
            x -= 1
            y += 1
        elif (x+1, y+1) not in grid:  # one step down and to the right
            x += 1
            y += 1
        else:
            return x,y,True

def simulate_falling_sand(grid):
    start_x, start_y = 500,0
    while True:
        x,y,at_rest = pour_sand(grid,start_x, start_y)
        grid[(x,y)] = 'o'
        if not at_rest:
            return grid
        else:
            grid[(x,y)] = 'o'


@timer
def main(filename: str) -> Solution:
    grid = process_input(filename)
    grid = simulate_falling_sand(grid)
    part_1_solution = len({k for k,v in grid.items() if v == 'o'}) - 1
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc14.txt")
    print(f"PART 1: {part_1_solution}")  # 1072
    print(f"PART 2: {part_2_solution}")  #
