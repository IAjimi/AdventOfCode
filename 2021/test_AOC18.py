from _utils import read_input
from AOC18 import main, compute_magnitude, get_final_sum

import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ],
)
def test_compute_magnitude(test_input, expected):
    assert compute_magnitude(test_input) == expected


def test_get_final_sum():
    _input = read_input("test_aoc18.txt")
    line = get_final_sum(_input)
    assert "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]" == line


def test_main():
    part_1, part_2 = main("test_aoc18.txt")
    assert part_1 == 4140
    assert part_2 == 3993

    part_1, part_2 = main("aoc18.txt")
    assert part_1 == 4116
    assert part_2 == 4638
