from AOC14 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc14.txt")
    assert test_part_1 == 1588
    assert test_part_2 == 2188189693529

    part_1, part_2 = main("aoc14.txt")
    assert part_1 == 2223
    assert part_2 == 2566282754493
