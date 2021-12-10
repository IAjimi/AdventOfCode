from AOC10 import main


def test_main():
    test_part_1, test_part_2 = main("test_aoc10.txt")
    assert test_part_1 == 26397
    assert test_part_2 == 288957

    part_1, part_2 = main("aoc10.txt")
    assert part_1 == 367227
    assert part_2 == 3583341858
