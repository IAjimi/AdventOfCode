import os
import time


def read_input(filepath: str):
    """
    Open and read file at filepath, return list of integers.
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


def sign(num):
    if num == 0:
        return 0
    elif num < 0:
        return -1
    elif num > 0:
        return 1
