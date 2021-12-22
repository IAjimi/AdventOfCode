from AOC04 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc4.txt")
    assert test_part_1 == 4512
    assert test_part_2 == 1924

    part_1, part_2 = main("aoc4.txt")
    assert part_1 == 87456
    assert part_2 == 15561
