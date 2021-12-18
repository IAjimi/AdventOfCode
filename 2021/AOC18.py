"""
Bleh. Was stuck for 2-3 hours.
Ended up using a mix of 2 existing solutions:
    * regex parsing: https://www.reddit.com/r/adventofcode/comments/rizw2c/comment/hp11644/?utm_source=share&utm_medium=web2x&context=3
    * add function: https://github.com/benediktwerner/AdventOfCode/blob/master/2021/day18/sol.py
"""

from _utils import read_input, timer

import math
import re


def get_split(num: int):
    half = num / 2
    left_split = math.floor(half)
    right_split = math.ceil(half)
    return f"[{left_split},{right_split}]"


def sub(s, n, ind):
    matches = list(re.finditer("\d+", s))
    if matches:
        start, end = matches[ind].span()
        s = s[:start] + str(int(s[start:end]) + n) + s[end:]
    return s


def explode(line: str):
    for match in re.finditer("\[(\d+),(\d+)\]", line):
        pre, post = line[: match.start(0)], line[match.end(0) :]
        x, y = map(int, match.groups())
        if pre.count("[") - pre.count("]") >= 4:
            line = sub(pre, x, -1) + "0" + sub(post, y, 0)
            return True, line
    return False, line


def split(line: str):
    for match in re.finditer("\d+", line):
        pre, post = line[: match.start(0)], line[match.end(0) :]
        x = int(match.group())
        if x >= 10:
            line = pre + get_split(x) + post
            return True, line
    return False, line


def reduce(line: str):
    while True:
        change, line = explode(line)
        if change:
            continue
        change, line = split(line)
        if not change:
            break
    return line


def add(x: str, y: str):
    line = f"[{x},{y}]"
    return reduce(line)


def magnitude(line: str):
    for match in re.finditer("\[(\d+),(\d+)\]", line):
        pre, post = line[: match.start(0)], line[match.end(0) :]
        x, y = map(int, match.groups())
        new_val = 3 * x + 2 * y
        line = pre + str(new_val) + post
        return True, line
    return False, line


def compute_magnitude(line: str):
    while True:
        change, line = magnitude(line)
        if change:
            continue
        else:
            break
    return line


def maximize_magnitude(_input: list):
    max_m = 0

    for i in range(len(_input)):
        for j in range(len(_input)):
            if i != j:
                line = add(_input[i], _input[j])
                m = int(compute_magnitude(line))
                max_m = max(m, max_m)

    return max_m


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    line = _input[0]

    for ix, newline in enumerate(_input[1:]):
        line = add(line, newline)

    part_1_score = compute_magnitude(line)
    part_2_score = maximize_magnitude(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc18.txt")
    print(f"PART 1: {part_1_score}")  # 4116
    print(f"PART 2: {part_2_score}")  # 4638
