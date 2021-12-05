from AOC5 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc5.txt")
    assert test_part_1 == 5
    assert test_part_2 == 12

    part_1, part_2 = main("aoc5.txt")
    assert part_1 == 6710
    assert part_2 == 20121
