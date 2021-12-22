from AOC09 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc9.txt")
    assert test_part_1 == 15
    assert test_part_2 == 1134

    part_1, part_2 = main("aoc9.txt")
    assert part_1 == 532
    assert part_2 == 1110780
