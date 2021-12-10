"""
Got my best rank yet at 1191 for part 2!

Decided to use a dictionary counting the number of lanternfish
of a certain age to keep things light and quickly iterate over
different rounds.

Luckily the position of the lanternfish didn't play a role in either
part 1 or 2, which allowed me to complete part 2 without having to
change my code at all (besides adjusting the max number of turns).
"""

from _utils import read_input, count_occurrences, timer
from collections import defaultdict


def parse_input(_input: list):
    """
    Open and read file at filepath, return dictionary holding
    the number of lanternfish of a certain age.
    """
    _input = (int(i) for i in _input[0].split(","))  # only one line in input
    counter = count_occurrences(_input)
    return counter


def simulate_lanternfish_growth(counter: dict, max_days: int):
    """
    Return the total number of lanternfish after growing for
    max_days.
    """
    for t in range(max_days):
        new_counter = defaultdict(int)

        for age, n_lanternfish in counter.items():
            if age == 0:
                new_counter[
                    8
                ] = n_lanternfish  # not updated bc this is only case where new lanternfish are added
                new_counter[6] += n_lanternfish
            else:
                new_counter[age - 1] += n_lanternfish

        counter = new_counter

    total_n_lanternfish = sum(counter.values())
    return total_n_lanternfish


@timer
def main(filepath: str):
    """
    Returns solution for AOC day 6 from input filepath.
    """
    _input = read_input(filepath)
    counter = parse_input(_input)

    part_1_score = simulate_lanternfish_growth(counter, 80)
    part_2_score = simulate_lanternfish_growth(counter, 256)

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc6.txt")
    print(f"PART 1: {part_1_score}")  # 365862
    print(f"PART 2: {part_2_score}")  # 1653250886439
