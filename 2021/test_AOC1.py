from AOC1 import process_input, count_increase, count_sliding_window_increase


def test_count_increase():
    test_input = process_input("test_aoc1.txt")
    assert count_increase(test_input) == 7

    actual_input = process_input("aoc1.txt")
    assert count_increase(actual_input) == 1233


def test_count_sliding_window_increase():
    test_input = process_input("test_aoc1.txt")
    assert count_sliding_window_increase(test_input) == 5

    actual_input = process_input("aoc1.txt")
    assert count_sliding_window_increase(actual_input) == 1275
