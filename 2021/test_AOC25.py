from AOC25 import main


def test_main():
    part_1_score = main("test_aoc25.txt")
    assert part_1_score == 58

    part_1_score = main("aoc25.txt")
    assert part_1_score == 205
