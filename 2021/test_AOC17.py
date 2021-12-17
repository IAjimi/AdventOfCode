from AOC17 import ProbeLauncher


def test_main():
    part_1, part_2 = ProbeLauncher("test_aoc17.txt").main()
    assert part_1 == 45
    assert part_2 == 112

    part_1, part_2 = ProbeLauncher("aoc17.txt").main()
    assert part_1 == 3003
    assert part_2 == 940
