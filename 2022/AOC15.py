from typing import List, Tuple, Set

from _utils import read_input, timer, Solution


SENSOR, BEACON = 1, -1

Y = 2_000_000


def process_input(filename: str):
    _input = read_input(filename)

    import parse

    grid = set()
    empty = set()
    for line in _input:
        x1, y1, x2, y2 = tuple(
            parse.parse(
                "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", line
            ).fixed
        )
        grid.add((x1, y1))
        grid.add((x2, y2))

        distance = manhattan_distance((x1, y1), (x2, y2))
        distance_to_y = abs(y1 - Y)
        remaining_distance = distance - distance_to_y
        if remaining_distance >= 0:
            for dx in range(-remaining_distance, remaining_distance + 1):
                empty.add((x1 + dx, Y))

    for pos in grid:
        if pos in empty:
            empty.remove(pos)
    return len(empty)


def manhattan_distance(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return abs(x1 - x2) + abs(y1 - y2)


@timer
def main(filename: str) -> Solution:
    grid = process_input(filename)
    part_1_solution = grid
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc15.txt")
    print(f"PART 1: {part_1_solution}")  # 4907780
    print(f"PART 2: {part_2_solution}")  #
