from typing import Tuple, List, Dict

from _utils import read_input, timer, Score


def process_input(filepath: str) -> Tuple[Dict[int, List[str]], List[str]]:
    """
    Programmatically parsing the crates would've taken too much time so
    hardcoded my input instead (for now).
    """
    _input = read_input(filepath)
    crates = {
        1: ["D", "L", "J", "R", "V", "G", "F"],
        2: ["T", "P", "M", "B", "V", "H", "J", "S"],
        3: ["V", "H", "M", "F", "D", "G", "P", "C"],
        4: ["M", "D", "P", "N", "G", "Q"],
        5: ["J", "L", "H", "N", "F"],
        6: ["N", "F", "V", "Q", "D", "G", "T", "Z"],
        7: ["F", "D", "B", "L"],
        8: ["M", "J", "B", "S", "V", "D", "N"],
        9: ["G", "L", "D"],
    }
    # crates = {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"]}  # test input
    return crates, _input[10:]


def process_instructions(filename: str, reverse_crates: bool) -> str:
    crates, instructions = process_input(filename)
    for line in instructions:
        _, n_crates, _, initial_crate, _, new_crate = line.split(" ")
        n_crates = int(n_crates)
        initial_crate = int(initial_crate)
        new_crate = int(new_crate)

        moved_crates = crates[initial_crate][-n_crates:]
        crates[initial_crate] = crates[initial_crate][
            : len(crates[initial_crate]) - n_crates
        ]
        crates[new_crate] += moved_crates[::-1] if reverse_crates else moved_crates
    return "".join([l[-1] for l in crates.values()])


@timer
def main(filename: str) -> Score:
    part_1_score = process_instructions(filename, True)
    part_2_score = process_instructions(filename, False)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc5.txt")
    print(f"PART 1: {part_1_score}")  # QMBMJDFTD
    print(f"PART 2: {part_2_score}")  # NBTVTJNFJ
