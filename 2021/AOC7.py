"""
Completed in <10 minutes. Needs cleaning + optimization (better data structure
than list).
"""

from _utils import read_input, timer


def part_1(_input):
    max_position = max(_input)

    fuel_needed = {}

    for target_pos in range(max_position):
        total = sum([abs(cur_pos - target_pos) for cur_pos in _input])
        fuel_needed[target_pos] = total

    return min(fuel_needed.values())


def total_sum(n):
    return n * (n + 1) // 2


def part_2(_input):
    max_position = max(_input)

    fuel_needed = {}

    for target_pos in range(max_position):
        total = [total_sum(abs(1 + cur_pos - target_pos)) for cur_pos in _input]
        fuel_needed[target_pos] = sum(total)

    return min(fuel_needed.values())


@timer
def main(filepath: str):
    _input = read_input(filepath)
    _input = [int(i) for i in _input[0].split(",")]
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc7.txt")
    print(f"PART 1: {part_1_score}")  # 356992
    print(f"PART 2: {part_2_score}")  # 101268110
