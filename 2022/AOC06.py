from collections import defaultdict

from _utils import read_input, timer, Solution


def process_input(filepath: str) -> str:
    _input = read_input(filepath)
    return _input[0]


def detect_message(_input: str, n_distinct: int) -> int:
    """
    Returns the first position where the n_distinct last characters are all different
    """
    counter = defaultdict(int)

    for i, char in enumerate(_input):
        counter[char] += 1

        if i >= n_distinct:
            counter[_input[i - n_distinct]] -= 1

            if max(counter.values()) <= 1:
                return i + 1

    return len(_input)


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    part_1_solution = detect_message(_input, n_distinct=4)
    part_2_solution = detect_message(_input, n_distinct=14)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc6.txt")
    print(f"PART 1: {part_1_solution}")  # 1134
    print(f"PART 2: {part_2_solution}")  # 2263
