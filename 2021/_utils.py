import os
import time

from collections import defaultdict

from typing import Dict, List, Tuple

Point = Tuple[int, int]
GridDict = Dict[Point, int]


def read_input(filepath: str) -> List[str]:
    """
    Open and read file at filepath, return list of strings.
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_path, filepath)

    with open(filepath) as _input:
        return _input.read().splitlines()


def timer(func):
    """
    Decorator copied from https://www.geeksforgeeks.org/timing-functions-with-decorators-python/
    """

    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s.")
        return result

    return wrap_func


def sign(num: int) -> int:
    if num == 0:
        return 0
    elif num < 0:
        return -1
    else:
        return 1


def create_grid(_input: list) -> GridDict:
    """
    Turns raw input into a grid dict (key: position).
    """
    _input = [[int(char) for char in line] for line in _input]
    grid = {
        (x, y): _input[y][x] for y in range(len(_input)) for x in range(len(_input[0]))
    }
    return grid


def count_occurrences(_input: List[int]) -> Dict[int, int]:
    """
    Return number of occurrences of all values in
    _input.
    """
    counter = defaultdict(int)
    for num in _input:
        counter[num] += 1
    return counter


def get_median(lst: List[int]) -> int:
    """
    Return median value of an unsorted list.
    """
    lst.sort()
    return lst[len(lst) // 2]


def product(lst: list) -> int:
    result = 1
    for num in lst:
        result *= num
    return result
