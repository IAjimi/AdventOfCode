from AOC21 import Game, QuantumGame


def test_main():
    test_filepath = "test_aoc21.txt"
    part_1_score = Game(test_filepath).main()
    assert part_1_score == 1190820

    part_2_score = QuantumGame(test_filepath).main()
    assert part_2_score == 444356092776315

    input_filepath = "aoc21.txt"
    part_1_score = Game(input_filepath).main()
    assert part_1_score == 757770

    part_2_score = QuantumGame(input_filepath).main()
    assert part_2_score == 712381680443927
