from _utils import read_input, timer, Score


def get_score(char) -> int:
    if char.islower():
        return 1 + ord(char) - ord("a")
    else:
        return 27 + ord(char) - ord("A")


def part_1(_input) -> int:
    total = 0

    for rucksack in _input:
        first_half_index = len(rucksack) // 2
        rucksack1 = set(rucksack[:first_half_index])
        rucksack2 = set(rucksack[first_half_index:])
        dupe = rucksack1 & rucksack2
        total += sum({get_score(char) for char in dupe})
    return total


def part_2(_input) -> int:
    total = 0

    for group_id in range(0, len(_input), 3):
        rucksack1 = set(_input[group_id])
        rucksack2 = set(_input[group_id+1])
        rucksack3 = set(_input[group_id+2])
        dupe = rucksack1 & rucksack2 & rucksack3
        total += sum({get_score(c) for c in dupe})
    return total


@timer
def main(filename: str) -> Score:
    _input = read_input(filename)
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc3.txt")
    print(f"PART 1: {part_1_score}")  # 7824
    print(f"PART 2: {part_2_score}")  # 2798
