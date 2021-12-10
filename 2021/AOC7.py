"""
Completed in <10 minutes
"""

from _utils import read_input, timer, count_occurrences


def total_sum(n):
    """
    Sum of all numbers from 0 to n.

    Used for the fuel computation in part 2, where n is the distance between
    two points.
    """
    return n * (n + 1) // 2


def solver(counter: dict, part_1: bool):
    fuel_needed = 10 ** 16
    max_position = max(counter.keys())

    for target_pos in range(max_position):
        if part_1:
            total = sum(
                [n * abs(cur_pos - target_pos) for cur_pos, n in counter.items()]
            )
        else:
            total = sum(
                [
                    n * total_sum(abs(1 + cur_pos - target_pos))
                    for cur_pos, n in counter.items()
                ]
            )

        fuel_needed = min(fuel_needed, total)

    return fuel_needed


@timer
def main(filepath: str):
    _input = read_input(filepath)
    _input = [int(i) for i in _input[0].split(",")]
    counter = count_occurrences(_input)
    part_1_score = solver(counter, part_1=True)
    part_2_score = solver(counter, part_1=False)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc7.txt")
    print(f"PART 1: {part_1_score}")  # 356992
    print(f"PART 2: {part_2_score}")  # 101268110
