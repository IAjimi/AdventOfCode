from AOC22 import main


def test_main():
    part_1_score, part_2_score = main("test_aoc22.txt")
    assert part_1_score == 474140
    assert part_2_score == 2758514936282235

    part_1_score, part_2_score = main("aoc22.txt")
    assert part_1_score == 587785
    assert part_2_score == 1167985679908143
