"""
Part 1 completed at 00:23:49, rank 1072.
Very straightforward!
"""

from typing import Tuple, Set
from collections.abc import Callable

from _utils import read_input, timer, Point


def parse_input(filepath: str) -> Tuple[Set[Point], Set[Point], int, int]:
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


def move_sea_cucumber_herd(
    current_herd: Set[Point], other_herd: Set[Point], move_func: Callable[Point, Point]
) -> Tuple[bool, Set[Point]]:
    changed = False
    new_herd = current_herd.copy()

    for pos in current_herd:
        # get next location of sea cucumber
        next_pos = move_func(pos)

        # move if new space is empty
        if next_pos not in current_herd and next_pos not in other_herd:
            new_herd.remove(pos)
            new_herd.add(next_pos)
            changed = True

    return changed, new_herd


def migrate(
    horizontal: Set[Point], vertical: Set[Point], width: int, height: int
) -> Tuple[bool, Set[Point], Set[Point]]:
    """
    Return changed position of east-facing and south-facing sea
    cucumbers.
    """
    # move all east-facing sea cucumbers
    move_func = lambda x: ((x[0] + 1) % width, x[1])
    hor_changed, horizontal = move_sea_cucumber_herd(horizontal, vertical, move_func)

    # consider all south-facing sea cucumbers
    move_func = lambda x: (x[0], (x[1] + 1) % height)
    ver_changed, vertical = move_sea_cucumber_herd(vertical, horizontal, move_func)

    # update bool to account for both
    changed = hor_changed or ver_changed

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
