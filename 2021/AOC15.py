"""
Spent most of the time figuring out how to properly expand
the grid in part 2. Runs in += 1.2 seconds for both parts,
with bottleneck in part 2 Dijkstra.
"""

from _utils import read_input, timer


import heapq


def parse_input(_input: list):
    grid_size = len(_input)
    grid = {
        (x, y): int(_input[y][x]) for y in range(grid_size) for x in range(grid_size)
    }
    return grid, grid_size


def get_neighbors(grid: dict, pos: tuple):
    """
    Returns neighbors of a tile if only allowed movements
    are up, left, right, down (no diagonals).
    """
    x, y = pos
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = [n for n in neighbors if n in grid]
    return neighbors


def least_risky_path(grid: dict, start: tuple, end: tuple):
    """
    Returns risk level of least risky path. Djikstra algorithm.
    """
    queue = []
    heapq.heappush(queue, (-grid[start], start))  # risk level of 1st node doesn't count
    visited = set()

    while queue:
        risk_level, current_node = heapq.heappop(queue)
        risk_level += grid[current_node]

        if current_node == end:
            return risk_level
        elif current_node not in visited:
            visited.add(current_node)

            neighbors = get_neighbors(grid, current_node)
            for next_node in neighbors:
                if next_node not in visited:
                    heapq.heappush(queue, (risk_level, next_node))

    return -1


def create_tiles(grid: dict):
    """
    Returns all 9 tiles in a dict.
    The values in each tile in all 1 higher than
    those in the previous tile, with a max of 9.
    """
    tiles = {0: grid.copy()}

    for dx in range(9):
        prev_grid = tiles[dx]
        new_grid = {pos: val + 1 if val < 9 else 1 for pos, val in prev_grid.items()}
        tiles[dx + 1] = new_grid

    return tiles


def expand_grid(tiles: dict, grid: dict, grid_size: int):
    """
    Returns expanded grid dict.

    Grabs appropriate tile, adjusts positions within, adds to
    grid dict.
    """
    grid_size -= 1

    for dx in range(5):
        for dy in range(5):
            key = dx + dy
            for pos, val in tiles[key].items():
                new_x = pos[0] if dx == 0 else pos[0] + ((1 + grid_size) * dx)
                new_y = pos[1] if dy == 0 else pos[1] + ((1 + grid_size) * dy)
                grid[new_x, new_y] = val
    return grid


def part_2(grid: dict, grid_size: int):
    """
    Returns part 2 solution.

    First generates all 9 distinct tiles.

    Because each position appears 25 times, 1x per tile,
    with a value higher by one than the tile above / left
    of it, the new extended grid is made out of repeating
    tiles:
        0  1  2  3  4
        1  2  3  4  5
        2  3  4  5  6
        3  4  5  6  7
        4  5  6  7  8

    The tiles have adjusted values, not adjusted positions.

    Once we have all 9 tiles, we expand the grid by
    simply adding adjusting the tiles with adjusted positions
    to account for the tile's placement to the existing grid.

    The final step is to run Djikstra (least_risky_path).
    """
    tiles = create_tiles(grid)
    grid = expand_grid(tiles, grid, grid_size)

    expanded_grid_size = max([x for x, y in grid.keys()])
    end = expanded_grid_size, expanded_grid_size

    part_2_score = least_risky_path(grid, start=(0, 0), end=end)
    return part_2_score


@timer
def main(filepath: str):
    _input = read_input(filepath)
    grid, grid_size = parse_input(_input)

    end = grid_size - 1, grid_size - 1
    part_1_score = least_risky_path(grid, start=(0, 0), end=end)

    part_2_score = part_2(grid, grid_size)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc15.txt")
    print(f"PART 1: {part_1_score}")  # 811
    print(f"PART 2: {part_2_score}")  # 3012
