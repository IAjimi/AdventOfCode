from _utils import read_input, timer

from collections import defaultdict


def process_input(line):
    """
    Returns a tuple of x,y coordinates from a line of the input.

    Ex:
        process_input("0,9 -> 5,9")
        > ([0,9], [5,9])
    """
    coords1, coords2 = line.split(" -> ")
    coords1 = [int(i) for i in coords1.split(",")]
    coords2 = [int(i) for i in coords2.split(",")]
    return coords1, coords2


def turn_lines_to_points(line):
    """
    Return all the lines between two points, start and end points included.
    """
    coords1, coords2 = line
    x1, y1 = coords1
    x2, y2 = coords2

    if x1 == x2:
        abs_dist = abs(y2 - y1)
        y_dir = 1 if y2 > y1 else -1
        return [(x1, y1 + r * y_dir) for r in range(abs_dist + 1)]
    elif y1 == y2:
        abs_dist = abs(x2 - x1)
        x_dir = 1 if x2 > x1 else -1
        return [(x1 + r * x_dir, y1) for r in range(abs_dist + 1)]
    else:
        # Diagonal lines, always at 45 degree angle
        abs_dist = abs(x2 - x1)
        x_dir = 1 if x2 > x1 else -1
        y_dir = 1 if y2 > y1 else -1
        return [(x1 + r * x_dir, y1 + r * y_dir) for r in range(abs_dist + 1)]


def count_overlapping_lines(_input: list):
    """
    Returns the number of points that have 2 lines
    going through them or more.
    """
    counter = defaultdict(int)
    for line in _input:
        points_list = turn_lines_to_points(line)
        for point in points_list:
            counter[point] += 1

    filtered_points = [k for k, v in counter.items() if v >= 2]
    return len(filtered_points)


@timer
def main(filepath: str):
    """
    Returns solution for AOC day 5 from input filepath.
    """
    _input = read_input(filepath)
    _input = [process_input(line) for line in _input]

    part_1_input = [
        line for line in _input if line[0][0] == line[1][0] or line[0][1] == line[1][1]
    ]
    part_1_score = count_overlapping_lines(part_1_input)
    part_2_score = count_overlapping_lines(_input)

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc5.txt")
    print(f"PART 1: {part_1_score}")  # 6710
    print(f"PART 2: {part_2_score}")  # 20121
