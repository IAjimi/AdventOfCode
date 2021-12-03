from _utils import read_input

def process_input(filepath: str):
    """
    Open and read file at filepath, return list of integers.
    """
    _input = read_input(filepath)
    return [int(i) for i in _input]


def count_increase(_input: list):
    """
    Returns the number of times a number in the _input
    list is bigger than its predecessor.
    """
    counter = 0

    for i in range(1, len(_input)):
        curr = _input[i]
        prev = _input[i - 1]

        if curr > prev:
            counter += 1

    return counter


def count_sliding_window_increase(_input: list):
    """
    Returns the number of times a sequence of 3 integers
    in the _input list is bigger than the previous sequence.

    Because such a list always has two numbers in common, this
    is equivalent to comparing the 1st number of the previous
    sequence to the last number of the new sequence.

    Those numbers are shown in parenthesis below:
     0  1  2  3
    (x) x  x
        x  x (x)
    """
    counter = 0

    for i in range(1, len(_input) - 2):
        curr = _input[i + 2]
        prev = _input[i - 1]

        if curr > prev:
            counter += 1

    return counter


if __name__ == "__main__":
    _input = read_input("2021/aoc1.txt")

    counter = count_increase(_input)
    print(f"PART 1: {counter}")  # 1233

    counter = count_sliding_window_increase(_input)
    print(f"PART 2: {counter}")  # 1275
