from typing import List, Tuple, Set

from _utils import read_input, timer, Solution, Point


def process_input(filename: str):
    _input = read_input(filename)
    return _input


def get_neighbors(head: Point, tail: Point) -> bool:
    x, y = head
    neighbors = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    return tail in neighbors


def move_head(direction: str, x: int, y: int) -> Point:
    if direction == "R":
        x += 1
    elif direction == "L":
        x -= 1
    elif direction == "U":
        y -= 1
    elif direction == "D":
        y += 1
    return x, y


def adjust_tail(head: Point, tail: Point) -> Point:
    x, y = head
    x2, y2 = tail

    if get_neighbors(head, tail):
        return tail
    elif (y == y2) and x2 - x == 2:
        x2 -= 1  # right
    elif (y == y2) and x - x2 == 2:
        x2 += 1  # left
    elif (x == x2) and y - y2 == 2:
        y2 += 1  # down
    elif (x == x2) and y2 - y == 2:
        y2 -= 1  # up
    elif x > x2 and y < y2:  # top right
        x2 += 1  # right
        y2 -= 1  # up
    elif x > x2 and y > y2:  # bottom right
        x2 += 1  # right
        y2 += 1  # down
    elif x < x2 and y > y2:  # bottom left
        x2 -= 1  # left
        y2 += 1  # down
    elif x < x2 and y < y2:  # top left
        x2 -= 1  # left
        y2 -= 1  # up
    else:
        raise Exception

    return (x2, y2)


def simulate(_input: List[str], len_rope: int = 2) -> int:
    knots = [(0, 0) for i in range(len_rope)]
    visited = set()

    for line in _input:
        direction, step = line.split(" ")
        for r in range(int(step)):
            new_knots = [k for k in knots]
            new_knots[0] = move_head(direction, *new_knots[0])
            for i in range(1, len_rope):
                new_knots[i] = adjust_tail(new_knots[i - 1], new_knots[i])
            visited.add(new_knots[-1])
            knots = new_knots
    return len(visited)


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    part_1_solution = simulate(_input, len_rope=2)
    part_2_solution = simulate(_input, len_rope=10)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc9.txt")
    print(f"PART 1: {part_1_solution}")  # 6470
    print(f"PART 2: {part_2_solution}")  # 2658
