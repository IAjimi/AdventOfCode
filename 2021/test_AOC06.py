from AOC06 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc6.txt")
    assert test_part_1 == 5934
    assert test_part_2 == 26984457539

    part_1, part_2 = main("aoc6.txt")
    assert part_1 == 365862
    assert part_2 == 1653250886439
