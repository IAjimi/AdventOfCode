"""
00:17:00, rank 1326 for part 1.

So much debugging for part 2! My first instinct was to store cubes
instead of points, then compute their volume... But I was beset by
off-by-one errors and various bugs throughout.
"""
from typing import Tuple, List, Set

from _utils import read_input, timer

import parse

Point = Tuple[int, int, int]
Cube = Tuple[int, int, int, int, int, int]


def volume(cube: Cube) -> int:
    x1, x2, y1, y2, z1, z2 = cube
    return (1 + x2 - x1) * (1 + y2 - y1) * (1 + z2 - z1)


def parse_line(line: str) -> Tuple[bool, Cube]:
    switch_str, x1, x2, y1, y2, z1, z2 = tuple(
        parse.parse("{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}", line).fixed
    )
    is_on = True if switch_str == "on" else False
    return is_on, (x1, x2, y1, y2, z1, z2)


def parse_input(filepath: str) -> List[Tuple[bool, Cube]]:
    _input = read_input(filepath)
    return [parse_line(line) for line in _input]


def process_reboot_instruction(
    grid: Set[Point], is_on: bool, coords: Cube
) -> Set[Point]:
    """
    Adds / removes points within a cube to grid.
    """
    x1, x2, y1, y2, z1, z2 = coords

    if -50 <= x1 <= x2 <= 50 and -50 <= x1 <= x2 <= 50 and -50 <= x1 <= x2 <= 50:
        points = [
            (x, y, z)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        ]
        for p in points:
            if is_on and p not in grid:
                grid.add(p)
            elif not is_on and p in grid:
                grid.remove(p)

    return grid


def intersection(cube1: Cube, cube2: Cube) -> bool:
    """
    Returns True if both cubes intersect, otherwise False.
    """
    x1, x2, y1, y2, z1, z2 = cube1
    x3, x4, y3, y4, z3, z4 = cube2

    x_out_of_bounds = (x1 > x4) or (x3 > x2)
    y_out_of_bounds = (y1 > y4) or (y3 > y2)
    z_out_of_bounds = (z1 > z4) or (z3 > z2)

    if x_out_of_bounds or y_out_of_bounds or z_out_of_bounds:
        return False
    else:
        return True


def cut_cube(existing_cube: Cube, new_cube: Cube) -> List[Cube]:
    """
    Returns list of cubes that are in new_cube but not in existing_cube.
    """
    x1, x2, y1, y2, z1, z2 = existing_cube
    x3, x4, y3, y4, z3, z4 = new_cube

    cut_cubes = []

    new_min_x = max(x1, x3)
    new_max_x = min(x2, x4)
    new_min_y = max(y1, y3)
    new_max_y = min(y2, y4)

    # chop off left
    if x3 < x1:
        cut_cubes.append([x3, x1 - 1, y3, y4, z3, z4])
    # chop off right
    if x4 > x2:
        cut_cubes.append([x2 + 1, x4, y3, y4, z3, z4])
    # chop off bottom
    if y3 < y1:
        cut_cubes.append([new_min_x, new_max_x, y3, y1 - 1, z3, z4])
    # chop off top
    if y4 > y2:
        cut_cubes.append([new_min_x, new_max_x, y2 + 1, y4, z3, z4])
    # chop off back
    if z3 < z1:
        cut_cubes.append([new_min_x, new_max_x, new_min_y, new_max_y, z3, z1 - 1])
    # chop off front
    if z4 > z2:
        cut_cubes.append([new_min_x, new_max_x, new_min_y, new_max_y, z2 + 1, z4])

    return cut_cubes


def part_1(_input) -> int:
    """
    Naive solution. Keeps points in set, adds / removes
    depending on on/off switch.
    """
    grid = set()
    for is_on, coords in _input:
        process_reboot_instruction(grid, is_on, coords)

    part_1_score = len(grid)
    return part_1_score


def part_2(_input):
    """
    Returns total volume of all "on" cubes.

    Had to switch tracks for part 2, given that the
    number of points in cubes would've broken my computer.

    New approach is to keep track of all distinct cubes:
    * For every cube in the input, consider current cube.
    * If current cube is "on", add cube to cube universe.
    * Then, for all previously processed cubes, add difference
    of current and previous cube to cube universe.
    """
    cubes = []
    for is_on, this_cube in _input:
        new_cubes = [this_cube] if is_on else []
        for other_cube in cubes:
            if intersection(this_cube, other_cube):
                new_cubes.extend(cut_cube(this_cube, other_cube))
            else:
                new_cubes.append(other_cube)
        cubes = new_cubes

    part_2_score = sum((volume(c) for c in cubes))
    return part_2_score


@timer
def main(filepath: str) -> Tuple[int, int]:
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = parse_input(filepath)

    part_1_score = part_1(_input)
    part_2_score = part_2(_input)

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc22.txt")
    print(f"PART 1: {part_1_score}")  # 587785
    print(f"PART 2: {part_2_score}")  # 1167985679908143
