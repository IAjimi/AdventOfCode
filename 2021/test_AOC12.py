from AOC12 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc12.txt")
    assert test_part_1 == 10
    assert test_part_2 == 36

    test_part_1, test_part_2 = main("test_aoc12b.txt")
    assert test_part_1 == 19
    assert test_part_2 == 103

    test_part_1, test_part_2 = main("test_aoc12c.txt")
    assert test_part_1 == 226
    assert test_part_2 == 3509

    part_1, part_2 = main("aoc12.txt")
    assert part_1 == 3485
    assert part_2 == 85062
