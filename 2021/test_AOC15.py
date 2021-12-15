from AOC15 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc15.txt")
    assert test_part_1 == 40
    assert test_part_2 == 315

    part_1, part_2 = main("aoc15.txt")
    assert part_1 == 811
    assert part_2 == 3012
