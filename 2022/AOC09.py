from typing import List

from _utils import read_input, timer, Solution, Point, sign


def are_neighbors(head: Point, tail: Point) -> bool:
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
    else:
        raise NotImplementedError(f"Unrecognized direction: {direction}.")
    return x, y


def adjust_tail(head: Point, tail: Point) -> Point:
    if are_neighbors(head, tail):
        return tail
    else:
        x1, y1 = head
        x2, y2 = tail
        x2 += sign(x1 - x2)
        y2 += sign(y1 - y2)
        return (x2, y2)


def simulate(_input: List[str], len_rope: int = 2) -> int:
    knots = [(0, 0) for i in range(len_rope)]
    visited = set()

    for line in _input:
        direction, step = line.split(" ")
        for r in range(int(step)):
            knots[0] = move_head(direction, *knots[0])
            for i in range(1, len_rope):
                knots[i] = adjust_tail(knots[i - 1], knots[i])
            visited.add(knots[-1])
    return len(visited)


@timer
def main(filename: str) -> Solution:
    _input = read_input(filename)
    part_1_solution = simulate(_input, len_rope=2)
    part_2_solution = simulate(_input, len_rope=10)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc9.txt")
    print(f"PART 1: {part_1_solution}")  # 6470
    print(f"PART 2: {part_2_solution}")  # 2658
