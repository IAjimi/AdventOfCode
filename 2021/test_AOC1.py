from AOC1 import read_input, count_increase, count_sliding_window_increase


def test_count_increase():
    test_input = read_input("2021/test_aoc1.txt")
    assert count_increase(test_input) == 7


def test_count_sliding_window_increase():
    test_input = read_input("2021/test_aoc1.txt")
    assert count_sliding_window_increase(test_input) == 5
