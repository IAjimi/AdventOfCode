from AOC2 import process_input, part_1, part_2


def test_part_1():
    test_input = process_input("test_aoc2.txt")
    assert part_1(test_input) == 150

    actual_input = process_input("aoc2.txt")
    assert part_1(actual_input) == 1746616


def test_part_2():
    test_input = process_input("test_aoc2.txt")
    assert part_2(test_input) == 900

    actual_input = process_input("aoc2.txt")
    assert part_2(actual_input) == 1741971043
