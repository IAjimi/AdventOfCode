import heapq
from collections import defaultdict
from typing import List, Tuple, Set

from _utils import read_input, timer, Solution, Point

LEFT, RIGHT, UP, DOWN = (-1, 0), (1, 0), (0, -1), (0, 1)
CHAR_MAPPING = {"<": LEFT, ">": RIGHT, "^": UP, "v": DOWN}


def process_input(filename: str):
    _input = read_input(filename)
    grid = set()
    blizzards = defaultdict(list)  # position, characters
    for y, line in enumerate(_input):
        for x, char in enumerate(line):
            if char == "#":
                continue

            grid.add((x, y))

            if char in CHAR_MAPPING:
                blizzards[(x, y)].append(CHAR_MAPPING[char])

    return grid, blizzards


def move_blizzards(grid, blizzards):
    new_blizzards = defaultdict(list)

    for pos, bzz_list in blizzards.items():
        x, y = pos
        for bzz in bzz_list:
            (dx, dy) = bzz
            new_pos = (x + dx, y + dy)
            # handle hitting wall
            if new_pos not in grid:
                if bzz == LEFT:
                    new_pos = max(x for x, y in grid), y
                elif bzz == RIGHT:
                    new_pos = min(x for x, y in grid), y
                elif bzz == UP:
                    new_pos = x, max(y for x, y in grid) - 1
                elif bzz == DOWN:
                    new_pos = x, min(y for x, y in grid) + 1
            new_blizzards[new_pos].append(bzz)

    return new_blizzards


def get_neighbors(pos) -> List[Point]:
    x, y = pos
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return neighbors


def shortest_path(grid, blizzards_timelapse, start, end, start_time=0) -> int:
    """
    Returns shortest path to destination. Djikstra algorithm.
    """
    queue = []
    heapq.heappush(queue, (start_time, start))
    visited = set()

    while queue:
        minutes, current_node = heapq.heappop(queue)
        if (minutes, current_node) in visited:
            continue
        else:
            visited.add((minutes, current_node))

        visited.add((minutes, current_node))
        current_blizzards = blizzards_timelapse[minutes]

        if current_node == end:
            return minutes - start_time - 1

        # try moving
        neighbors = get_neighbors(current_node)
        for next_node in neighbors:
            if (
                next_node in grid
                and next_node not in current_blizzards
                and next_node not in visited
            ):
                heapq.heappush(queue, (minutes + 1, next_node))

        # stay put
        if current_node not in blizzards_timelapse[minutes]:
            heapq.heappush(queue, (minutes + 1, current_node))

    return -1


def print_grid(grid) -> str:
    grid_str = ""
    max_x = max(pos[0] for pos in grid)
    max_y = max(pos[1] for pos in grid)

    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            if len(grid[(x, y)]) == 0:
                line += "."
            elif len(grid[(x, y)]) == 1:
                move = grid[(x, y)][0]
                if move == LEFT:
                    line += "<"
                elif move == RIGHT:
                    line += ">"
                elif move == UP:
                    line += "^"
                elif move == LEFT:
                    line += "v"
            else:
                line += str(len(grid[(x, y)]))

        grid_str += " ".join(line)
        grid_str += "\n"

    return grid_str


@timer
def main(filename: str) -> Solution:
    grid, blizzards = process_input(filename)

    blizzards_timelapse = [blizzards]
    # TODO find cycle
    for t in range(1000):
        new_blizzards = move_blizzards(grid, blizzards)
        blizzards_timelapse.append(new_blizzards)
        blizzards = new_blizzards

    max_y = max(y for x, y in grid)
    start = min(x for x, y in grid if y == 0), 0
    end = max(x for x, y in grid if y == max_y), max_y

    trip1 = shortest_path(grid, blizzards_timelapse, start, end)
    trip2 = shortest_path(grid, blizzards_timelapse, end, start, start_time=trip1)
    trip3 = shortest_path(
        grid, blizzards_timelapse, start, end, start_time=trip1 + trip2
    )
    part_1_solution = trip1
    part_2_solution = trip1 + trip2 + trip3
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc24.txt")
    print(f"PART 1: {part_1_solution}")  # 271
    print(f"PART 2: {part_2_solution}")  # 813
