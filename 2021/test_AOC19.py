from AOC19 import manhattan_distance, main


def test_manhattan_distance():
    coords1 = 1105, -1205, 1229
    coords2 = -92, -2380, -20
    assert abs(manhattan_distance(coords1, coords2)) == 3621


def test_main():
    part_1_score, part_2_score = main("test_aoc19.txt")
    assert part_1_score == 79
    assert part_2_score == 3621

    part_1_score, part_2_score = main("aoc19.txt")
    assert part_1_score == 392
    assert part_2_score == 13332
