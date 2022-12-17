from typing import List, Tuple, Set

from _utils import read_input, timer, Solution, Point

SHAPES = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    (
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
    ),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
]


def process_input(filename: str):
    _input = read_input(filename)

    jet_air = []
    for char in _input[0]:
        if char == ">":
            jet_air.append(1)
        else:
            jet_air.append(-1)
    return jet_air


def pushed_by_jet_air(rock: List[Point], dx: int) -> List[Point]:
    return [(x + dx, y) for x, y in rock]


def fall(rock: List[Point]) -> List[Point]:
    return [(x, y - 1) for x, y in rock]


def has_collided(rock: List[Point], chamber):
    if any([block in chamber for block in rock]):
        return True
    elif any([y == -1 for x, y in rock]):
        return True
    else:
        return False


def print_chamber(grid: Set[Point]) -> str:
    print("\n")
    print("--------------------------")
    grid_str = ""
    max_x = 7
    max_y = max(pos[1] for pos in grid)

    for y in range(max_y + 1):
        line = ["#" if (x, y) in grid else "." for x in range(max_x)]
        grid_str += " ".join(line)
        grid_str += "\n"

    print("--------------------------")
    return grid_str


def tetris(jet_air: List[int], max_rocks: int):
    max_y = -1
    jet_air_ix = 0
    rock_ix, rock_rounds, total_rocks = 0, 0, 0
    rock = [(x + 2, y + max_y + 4) for x, y in SHAPES[rock_ix]]
    chamber = {}
    while total_rocks <= max_rocks:
        # either push l/r or go down
        if rock_rounds % 2 == 0:
            jet_air_ix = jet_air_ix % len(jet_air)
            new_rock = pushed_by_jet_air(rock, jet_air[jet_air_ix])
            jet_air_ix += 1
        else:
            new_rock = fall(rock)

        # check for collision with wall
        if min(x for x, y in new_rock) < 0:
            new_rock = rock
        elif max(x for x, y in new_rock) > 6:
            new_rock = rock

        # check for collision with rock
        if has_collided(new_rock, chamber):
            # save prev rock position
            for block in rock:
                chamber[block] = "#"

            # manage state
            # print(print_chamber(chamber.keys()))
            total_rocks += 1
            rock_rounds = 0
            max_y = max(y for x, y in chamber)
            rock_ix = (rock_ix + 1) % len(SHAPES)
            rock = [(x + 2, y + max_y + 4) for x, y in SHAPES[rock_ix]]
        else:
            rock = new_rock
            rock_rounds += 1

    return chamber


@timer
def main(filename: str) -> Solution:
    jet_air = process_input(filename)
    chamber = tetris(jet_air, max_rocks=2022)
    part_1_solution = max(y for x, y in chamber)
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc17.txt")
    print(f"PART 1: {part_1_solution}")  #
    print(f"PART 2: {part_2_solution}")  #
