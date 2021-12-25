"""
Part 1 completed at 00:23:49, rank 1072.
Very straightforward!
"""

from typing import Tuple, Set

from _utils import read_input, timer, Point


def parse_input(filepath: str):
    _input = read_input(filepath)

    height = len(_input)
    width = len(_input[0])

    horizontal = set()
    vertical = set()

    for y in range(height):
        for x in range(width):
            if _input[y][x] == ">":
                horizontal.add((x, y))
            elif _input[y][x] == "v":
                vertical.add((x, y))

    return horizontal, vertical, width, height


def migrate(
    horizontal: Set[Point], vertical: Set[Point], width: int, height: int
) -> Tuple[bool, Set[Point], Set[Point]]:
    """
    Return changed position of east-facing and south-facing sea
    cucumbers.
    """
    changed = False

    # Consider all east-facing sea cucumbers
    new_horizontal = horizontal.copy()

    for pos in horizontal:
        # get next location of sea cucumber (wrap around if necessary)
        next_x = (pos[0] + 1) % width
        next_pos = (next_x, pos[1])

        # move if new space is empty
        if next_pos not in horizontal and next_pos not in vertical:
            new_horizontal.remove(pos)
            new_horizontal.add(next_pos)
            changed = True

    # update set after move
    horizontal = new_horizontal

    # consider all south-facing sea cucumbers
    new_vertical = vertical.copy()

    for pos in vertical:
        # get next location of sea cucumber (wrap around if necessary)
        next_y = (pos[1] + 1) % height
        next_pos = (pos[0], next_y)

        # move if new space is empty
        if next_pos not in horizontal and next_pos not in vertical:
            new_vertical.remove(pos)
            new_vertical.add(next_pos)
            changed = True

    vertical = new_vertical

    return changed, horizontal, vertical


def observe_migration(
    horizontal: Set[Point], vertical: Set[Point], width: int, height: int
) -> int:
    """
    Returns the number of steps after which the sea-cucumbers reach a steady-state.
    """
    step = 0

    while True:
        step += 1
        changed, horizontal, vertical = migrate(horizontal, vertical, width, height)

        if not changed:
            break

    return step


@timer
def main(filepath: str) -> int:
    """
     Returns part 1 score from a filepath.
    (Day 25 doesn't have a part 2.)
    """
    horizontal, vertical, width, height = parse_input(filepath)
    part_1_score = observe_migration(horizontal, vertical, width, height)

    return part_1_score


if __name__ == "__main__":
    part_1_score = main("aoc25.txt")
    print(f"PART 1: {part_1_score}")  # 305
