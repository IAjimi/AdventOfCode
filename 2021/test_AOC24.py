from AOC24 import Programs

negative_number_program = ["inp x", "mul x -1"]
multiple_checker_program = ["inp z", "inp x", "mul z 3", "eql z x"]


def test_negative_number():
    for r in range(-10, 10):
        registers = Programs(instr_list=negative_number_program, input_list=[r]).run()
        assert registers["w"] == 0
        assert registers["x"] == -r
        assert registers["y"] == 0
        assert registers["z"] == 0


import pytest


@pytest.mark.parametrize(
    "test_input,expected", [([1, 3], 1), ([-1, 3], 0), ([1, 2], 0)]
)
def test_multiple_checker(test_input, expected):
    registers = Programs(
        instr_list=multiple_checker_program, input_list=test_input
    ).run()
    assert registers["w"] == 0
    assert registers["y"] == 0
    assert registers["z"] == expected


def test_binary_converter():
    for r in range(0, 10):
        registers = Programs(filepath="test_aoc24.txt", input_list=[r]).run()
        bin_str = "{0:08b}".format(r)
        assert registers["w"] == int(bin_str[-3])
        assert registers["w"] == int(bin_str[-4])
        assert registers["y"] == int(bin_str[-2])
        assert registers["z"] == int(bin_str[-1])
