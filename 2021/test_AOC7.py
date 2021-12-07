from AOC7 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc7.txt")
    assert test_part_1 == 37
    assert test_part_2 == 168

    part_1, part_2 = main("aoc7.txt")
    assert part_1 == 356992
    assert part_2 == 101268110
