from _utils import read_input
from AOC03 import part_1, part_2


def test_part_1():
    test_input = read_input("test_aoc3.txt")
    assert part_1(test_input) == 198

    actual_input = read_input("aoc3.txt")
    assert part_1(actual_input) == 3958484


def test_part_2():
    test_input = read_input("test_aoc3.txt")
    assert part_2(test_input) == 230

    actual_input = read_input("aoc3.txt")
    assert part_2(actual_input) == 1613181
