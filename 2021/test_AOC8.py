from AOC8 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc8.txt")
    assert test_part_1 == 26
    assert test_part_2 == 61229

    part_1, part_2 = main("aoc8.txt")
    assert part_1 == 488
    assert part_2 == 1040429
