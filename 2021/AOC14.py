"""
Part 1 completed at 00:15:55, rank 2256.
Part 2 completed at 00:35:03, rank 1252.

Had to quickly refactor part 2 because part 1 had been done inefficiently
(dictionary with position, value). Realized positions were actually useless:
just needed to track *pairs*.
"""


from _utils import read_input, timer

from collections import defaultdict


def refactored_code(template: str, rules: dict, steps: int):
    template = {pos: letter for pos, letter in enumerate(template)}

    for step in range(1, steps + 1):
        new_template = {}
        jx = 0

        for ix in range(max(template.keys())):
            pair = template[ix] + template[ix + 1]
            new_val = rules[pair]

            new_template[jx] = template[ix]
            new_template[jx + 1] = new_val
            new_template[jx + 2] = template[ix + 1]

            jx += 2

        template = new_template

    from collections import Counter

    counter = Counter(template.values())
    most_common_count = counter.most_common(1)[0][1]
    least_common_count = counter.most_common()[-1][1]
    return most_common_count - least_common_count


def parse_rules(_input: list):
    rules = {}
    for line in _input:
        pair, new_letter = line.split(" -> ")
        rules[pair] = new_letter
    return rules


def create_pairs_counter(template: str):
    pairs_counter = defaultdict(int)
    for ix in range(len(template) - 1):
        letter1, letter2 = template[ix], template[ix + 1]
        pair = letter1 + letter2
        pairs_counter[pair] += 1

    return pairs_counter


def parse_input(_input: list):
    template, _input = _input[0], _input[2:]
    rules = parse_rules(_input)
    pairs_counter = create_pairs_counter(template)
    return rules, pairs_counter


def get_solution(pairs_counter: dict):
    """
    Returns difference in count between most and least
    common letter.

    Currently divides by 2 to get estimated number (since pair
    grouping means most letters get double-counted).
    """
    # Count letters
    counter = defaultdict(int)
    for pair, count in pairs_counter.items():
        counter[pair[0]] += count
        counter[pair[1]] += count

    # Do math (divide by 2 because storing pairs means same letter appears 2x)
    most_common_count = max(counter.values()) / 2
    least_common_count = min(counter.values()) / 2
    return most_common_count - least_common_count


def run_pair_insertion_program(rules: dict, pairs_counter: dict, steps: int):
    # Simulate pair insertion process for n steps
    for step in range(1, steps + 1):
        new_pairs = defaultdict(int)

        for pair, count in pairs_counter.items():
            new_letter = rules[pair]

            first_new_pair = pair[0] + new_letter
            second_new_pair = new_letter + pair[1]

            new_pairs[first_new_pair] += count
            new_pairs[second_new_pair] += count

        pairs_counter = new_pairs

    return get_solution(pairs_counter)


@timer
def main(filepath: str):
    _input = read_input(filepath)
    rules, pairs_counter = parse_input(_input)
    part_1_score = run_pair_insertion_program(rules, pairs_counter, steps=10)
    part_2_score = run_pair_insertion_program(rules, pairs_counter, steps=40)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc14.txt")
    print(f"PART 1: {part_1_score}")  # 2223
    print(f"PART 2: {part_2_score}")  # 2566282754493
