"""
Part 1 completed at 00:15:55, rank 2256.
Part 2 completed at 00:35:03, rank 1252.

Had to quickly refactor part 2 because part 1 had been done inefficiently
(dictionary with position, value). Realized positions were actually useless:
just needed to track *pairs*.
"""
from typing import Tuple, Dict, List

from _utils import read_input, timer

from collections import defaultdict


def parse_rules(_input: List[str]) -> Dict[str, str]:
    rules = {}
    for line in _input:
        pair, new_letter = line.split(" -> ")
        rules[pair] = new_letter
    return rules


def create_counters(template: str) -> Tuple[Dict[int, int], Dict[int, int]]:
    """
    Creates letter and pair counter dicts.
    Holds the counts of pairs and individual letters respectively.
    """
    pair_counter = defaultdict(int)
    letter_counter = defaultdict(int)
    letter_counter[template[0]] = 1  # for loop only counts 2nd letter

    for ix in range(len(template) - 1):
        letter1, letter2 = template[ix], template[ix + 1]
        pair = letter1 + letter2
        pair_counter[pair] += 1
        letter_counter[letter2] += 1
    return pair_counter, letter_counter


def parse_input(_input: list) -> Tuple[Dict[str, str], Dict[int, int], Dict[int, int]]:
    template, _input = _input[0], _input[2:]
    rules = parse_rules(_input)
    pair_counter, letter_counter = create_counters(template)
    return rules, pair_counter, letter_counter


def get_solution(letter_counter: dict) -> int:
    """
    Returns difference in count between most and least
    common letter.
    """
    most_common_count = max(letter_counter.values())
    least_common_count = min(letter_counter.values())
    return most_common_count - least_common_count


def run_pair_insertion_program(
    rules: dict,
    pair_counter: dict,
    letter_counter: dict,
    part_1_steps: int,
    part_2_steps: int,
) -> Tuple[int, int]:
    # Simulate pair insertion process for n steps
    for step in range(1, part_2_steps + 1):
        new_pair_counter = defaultdict(int)

        for pair, n in pair_counter.items():
            new_letter = rules[pair]

            first_new_pair = pair[0] + new_letter
            second_new_pair = new_letter + pair[1]

            new_pair_counter[first_new_pair] += n
            new_pair_counter[second_new_pair] += n

            letter_counter[new_letter] += n

        pair_counter = new_pair_counter
        if step == part_1_steps:
            part_1_score = get_solution(letter_counter)

    part_2_score = get_solution(letter_counter)

    return part_1_score, part_2_score


@timer
def main(filepath: str) -> Tuple[int, int]:
    _input = read_input(filepath)
    rules, pair_counter, letter_counter = parse_input(_input)
    part_1_score, part_2_score = run_pair_insertion_program(
        rules, pair_counter, letter_counter, part_1_steps=10, part_2_steps=40
    )
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc14.txt")
    print(f"PART 1: {part_1_score}")  # 2223
    print(f"PART 2: {part_2_score}")  # 2566282754493
