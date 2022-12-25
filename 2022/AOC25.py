from typing import List

from _utils import read_input, timer, Solution


def process_input(filename: str) -> List[int]:
    _input = read_input(filename)
    return _input


def snafu_to_real(line: str) -> int:
    num = 0

    for i, char in enumerate(reversed(line)):
        if char == "-":
            val = -1
        elif char == "=":
            val = -2
        else:
            val = int(char)

        num += val * (5 ** i)

    return num


def real_to_snafu(num: int) -> str:
    snafu = ""
    while num:
        remainder = num % 5
        if remainder in (0, 1, 2):
            snafu += str(remainder)
        elif remainder == 3:
            snafu += "="  # 2 away from 5
            num += 2
        elif remainder == 4:
            snafu += "-"  # 1 away from 5
            num += 1
        else:
            assert Exception

        num //= 5
    return snafu[::-1]


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    part_1_sum = sum([snafu_to_real(line) for line in _input])
    part_1_solution = real_to_snafu(part_1_sum)
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc25.txt")
    print(f"PART 1: {part_1_solution}")  # 2-==10===-12=2-1=-=0
    print(f"PART 2: {part_2_solution}")  # no part 2
