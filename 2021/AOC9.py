from _utils import read_input, timer


def get_neighbors(grid: dict, pos: tuple):
    x, y = pos
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    neighbors = [n for n in neighbors if n in grid]
    return neighbors


def find_low_points(grid: dict):
    low_points = []

    for pos, val in grid.items():
        neighbors = get_neighbors(grid, pos)
        neighbors_val = [grid[n] for n in neighbors]

        if val < min(neighbors_val):
            low_points.append(pos)

    return low_points


def bfs(grid: dict, point: tuple):
    queue = [point]
    visited = set()
    steps = 0

    while queue:
        current_loc = queue.pop()

        if current_loc not in visited:
            visited.add(current_loc)
            steps += 1

            neighbors = get_neighbors(grid, current_loc)
            neighbors = [n for n in neighbors if grid[n] < 9]
            queue.extend(neighbors)

    return steps


def part_1(grid: dict):
    low_points = find_low_points(grid)
    part_1_score = [grid[point] + 1 for point in low_points]
    return sum(part_1_score), low_points


def part_2(grid: dict, low_points: list):
    bassin_size = []

    for point in low_points:
        steps = bfs(grid, point)
        bassin_size.append(steps)

    bassin_size.sort()
    part_2_score = bassin_size[-3] * bassin_size[-2] * bassin_size[-1]
    return part_2_score


@timer
def main(filepath: str):
    _input = read_input(filepath)
    _input = [[int(char) for char in line] for line in _input]
    grid = {
        (x, y): _input[y][x] for y in range(len(_input)) for x in range(len(_input[0]))
    }

    part_1_score, low_points = part_1(grid)
    part_2_score = part_2(grid, low_points)

    return part_1_score, part_2_score


if __name__ == "__main__":
    # 7:00 - 07:10
    # 7:10 - 7:20
    part_1_score, part_2_score = main("aoc9.txt")
    print(f"PART 1: {part_1_score}")  # 532
    print(f"PART 2: {part_2_score}")  # 1110780
