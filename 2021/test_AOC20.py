from AOC20 import main


def test_main():
    part_1_score, part_2_score = main("aoc20.txt")
    assert  part_1_score == 5291
    assert part_2_score == 16665
