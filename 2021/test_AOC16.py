from AOC16 import main, get_solution

import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("9C0141080250320F1802104A08", (20, 1)),
        ("A0016C880162017C3686B18A3D4780", (31, 54)),
        ("C0015000016115A2E0802F182340", (23, 46)),
    ],
)
def test_get_solution(test_input, expected):
    assert get_solution(test_input) == expected


def test_main():
    part_1, part_2 = main("aoc16.txt")
    assert part_1 == 866
    assert part_2 == 1392637195518
