from typing import List, Set

from _utils import read_input, timer, Solution, product, Point


def process_input(filename: str) -> List[List[int]]:
    _input = read_input(filename)
    return [[int(i) for i in line] for line in _input]


def safe_max(l: List[int]) -> int:
    return max(l) if l else 0


def find_visible_trees(_input: List[List[int]]) -> Set[Point]:
    visible = set()
    max_x, max_y = len(_input[0]) - 1, len(_input) - 1

    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if x == 0 or x == max_x or y == 0 or y == max_y:
                visible.add((x, y))
            else:
                left_max = safe_max(_input[x][:y])
                right_max = safe_max(_input[x][y + 1:])
                top_max = safe_max([_input[i][y] for i in range(x)])
                bottom_max = safe_max([_input[i][y] for i in range(x + 1, max_x + 1)])
                if (
                    _input[x][y] > left_max
                    or _input[x][y] > right_max
                    or _input[x][y] > top_max
                    or _input[x][y] > bottom_max
                ):
                    visible.add((x, y))

    return visible


def compute_scenic_score(start: Point, _input: List[List[int]]) -> int:
    queue = [
        (0, (1, 0), start),
        (0, (-1, 0), start),
        (0, (0, 1), start),
        (0, (0, -1), start),
    ]
    height = _input[start[0]][start[1]]
    score = 1
    max_x, max_y = len(_input[0]) - 1, len(_input) - 1

    while queue:
        steps, dir, pos = queue.pop()
        x, y = pos[0] + dir[0], pos[1] + dir[1]

        if not (0 <= x <= max_x) or not (0 <= y <= max_y):
            score *= steps
        elif _input[x][y] >= height:
            score *= steps + 1
        else:
            queue.append((steps + 1, dir, (x, y)))

    return score


def find_best_view(_input: List[List[int]], visible_trees: Set[Point]) -> int:
    max_score = 0
    for pos in visible_trees:
        score = compute_scenic_score(pos, _input)
        max_score = max(max_score, score)
    return max_score


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    visible_trees = find_visible_trees(_input)
    part_1_solution = len(visible_trees)
    part_2_solution = find_best_view(_input, visible_trees)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc8.txt")
    print(f"PART 1: {part_1_solution}")  # 1779
    print(f"PART 2: {part_2_solution}")  # 172224
