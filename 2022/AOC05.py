from typing import Tuple, List

from _utils import read_input, timer, Solution


def process_input(filepath: str) -> Tuple[List[List[str]], List[str]]:
    """
    Programmatically parsing the crates would've taken too much time so
    hardcoded my input instead (for now).
    """
    _input = read_input(filepath)
    crates = [
        ["D", "L", "J", "R", "V", "G", "F"],
        ["T", "P", "M", "B", "V", "H", "J", "S"],
        ["V", "H", "M", "F", "D", "G", "P", "C"],
        ["M", "D", "P", "N", "G", "Q"],
        ["J", "L", "H", "N", "F"],
        ["N", "F", "V", "Q", "D", "G", "T", "Z"],
        ["F", "D", "B", "L"],
        ["M", "J", "B", "S", "V", "D", "N"],
        ["G", "L", "D"],
    ]
    # crates = [["Z", "N"], ["M", "C", "D"], ["P"]]  # test input
    return crates, _input[10:]


def parse_instruction(line: str) -> Tuple[int, int, int]:
    _, n_crates, _, initial_crate, _, new_crate = line.split(" ")
    return int(n_crates), int(initial_crate) - 1, int(new_crate) - 1


def process_instructions(filename: str, reverse_crates: bool) -> str:
    crates, instructions = process_input(filename)
    for line in instructions:
        n_crates, initial_crate, new_crate = parse_instruction(line)

        moved_crates = crates[initial_crate][-n_crates:]
        crates[initial_crate] = crates[initial_crate][
            : len(crates[initial_crate]) - n_crates
        ]
        crates[new_crate] += moved_crates[::-1] if reverse_crates else moved_crates
    return "".join([l[-1] for l in crates])


@timer
def main(filename: str) -> Solution:
    part_1_solution = process_instructions(filename, True)
    part_2_solution = process_instructions(filename, False)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc5.txt")
    print(f"PART 1: {part_1_solution}")  # QMBMJDFTD
    print(f"PART 2: {part_2_solution}")  # NBTVTJNFJ
