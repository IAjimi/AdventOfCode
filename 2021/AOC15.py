"""
Spent most of the time figuring out how to properly expand
the grid in part 2. Currently running a bit slow (+- 6s for
both parts).
"""

from _utils import read_input, timer


import queue


def get_neighbors(grid: dict, pos: tuple):
    x, y = pos
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = [n for n in neighbors if n in grid]
    return neighbors


def least_risky_path(grid: dict, start: tuple, end: tuple):
    q = queue.PriorityQueue()
    q.put((-grid[start], start))
    visited = set()

    while q.qsize() > 0:
        risk_level, current_node = q.get()
        risk_level += grid[current_node]

        if current_node == end:
            return risk_level
        elif current_node not in visited:
            visited.add(current_node)

            neighbors = get_neighbors(grid, current_node)
            for next_node in neighbors:
                q.put((risk_level, next_node))

    return -1


def create_grid(_input, grid_size):
    grid = {}
    for y in range(grid_size):
        for x in range(grid_size):
            grid[(x, y)] = int(_input[y][x])
    return grid


def create_tiles(grid: dict):
    tiles = {0: grid.copy()}

    for dx in range(9):
        prev_grid = tiles[dx]
        new_grid = {pos: val + 1 if val < 9 else 1 for pos, val in prev_grid.items()}
        tiles[dx + 1] = new_grid

    return tiles


def expand_grid(tiles: dict, grid: dict, grid_size: int):
    grid_size -= 1

    for dx in range(5):
        for dy in range(5):
            key = dx + dy
            for pos, val in tiles[key].items():
                new_x = pos[0] if dx == 0 else pos[0] + ((1 + grid_size) * dx)
                new_y = pos[1] if dy == 0 else pos[1] + ((1 + grid_size) * dy)
                grid[new_x, new_y] = val
    return grid


@timer
def main(filepath: str):
    _input = read_input(filepath)

    grid_size = len(_input)
    grid = create_grid(_input, grid_size)

    end = grid_size - 1, grid_size - 1
    part_1_score = least_risky_path(grid, start=(0, 0), end=end)

    # each position appears 25 times, 1x per tile
    tiles = create_tiles(grid)
    grid = expand_grid(tiles, grid, grid_size)

    expanded_grid_size = max([x for x, y in grid.keys()])
    end = expanded_grid_size, expanded_grid_size

    part_2_score = least_risky_path(grid, start=(0, 0), end=end)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc15.txt")
    print(f"PART 1: {part_1_score}")  # 811
    print(f"PART 2: {part_2_score}")  # 3012
