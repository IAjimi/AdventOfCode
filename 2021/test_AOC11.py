from AOC11 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc11.txt")
    assert test_part_1 == 1656
    assert test_part_2 == 195

    part_1, part_2 = main("aoc11.txt")
    assert part_1 == 1659
    assert part_2 == 227
