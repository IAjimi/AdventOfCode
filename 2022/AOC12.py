"""
A personal best: 00:09:16 (rank 179) for part 1, 00:12:42 (rank 225) for part 2.
Reused existing code from 2021 day 15.
"""

import heapq
from typing import List, Tuple

from _utils import read_input, timer, Solution, GridDict, Point


def process_input(filename: str) -> Tuple[Point, Point, GridDict]:
    _input = read_input(filename)
    grid = {}
    for x, line in enumerate(_input):
        for y, char in enumerate(line):
            if char == "S":
                start = x, y
                elevation = ord("a")
            elif char == "E":
                end = x, y
                elevation = ord("z")
            else:
                elevation = ord(char)

            grid[(x, y)] = elevation - ord("a")

    return start, end, grid


def get_neighbors(grid: GridDict, pos: Point) -> List[Point]:
    """
    Returns neighbors of a tile if only allowed movements
    are up, left, right, down (no diagonals).
    """
    x, y = pos
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = [n for n in neighbors if n in grid]
    return neighbors


def least_risky_path(grid: GridDict, start: Point, end: Point) -> int:
    """
    Returns shortest path to destination. Djikstra algorithm.
    """
    queue = []
    heapq.heappush(queue, (0, start))
    visited = set()

    while queue:
        steps, current_node = heapq.heappop(queue)
        elevation = grid[current_node]

        if current_node == end:
            return steps
        elif current_node not in visited:
            visited.add(current_node)

            neighbors = get_neighbors(grid, current_node)
            for next_node in neighbors:
                if next_node not in visited and grid[next_node] <= elevation + 1:
                    heapq.heappush(queue, (steps + 1, next_node))

    return -1


@timer
def main(filename: str) -> Solution:
    start, end, grid = process_input(filename)
    part_1_solution = least_risky_path(grid, start, end)
    starts = {k for k, v in grid.items() if v == 0}
    steps = [least_risky_path(grid, s, end) for s in starts]
    part_2_solution = min([s for s in steps if s > 0])
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc12.txt")
    print(f"PART 1: {part_1_solution}")  # 468
    print(f"PART 2: {part_2_solution}")  # 459
