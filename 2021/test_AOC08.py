from AOC08 import main, get_output_code
from _utils import read_input


def test_main():
    test_part_1, test_part_2 = main("test_aoc8.txt")
    assert test_part_1 == 26
    assert test_part_2 == 61229

    part_1, part_2 = main("aoc8.txt")
    assert part_1 == 488
    assert part_2 == 1040429


def test_get_output_code():
    test_input = read_input("test_aoc8.txt")
    expected_list = [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]
    zipped_list = zip(test_input, expected_list)
    for line, expected_int in zipped_list:
        assert get_output_code(line) == expected_int
