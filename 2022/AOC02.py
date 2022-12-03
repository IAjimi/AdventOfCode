from typing import Tuple, List

from _utils import read_input, timer


ROCK = 1
PAPER = 2
SCISSORS = 3
LOSES_TO = {
    ROCK: PAPER,
    SCISSORS: ROCK,
    PAPER: SCISSORS,
}  # cleaner as linked list?
WINS_AGAINST = {
    ROCK: SCISSORS,
    SCISSORS: PAPER,
    PAPER: ROCK,
}

WIN = 6
DRAW = 3
LOSS = 0


def decode_instruction(instr: str) -> int:
    if instr in ("A", "X"):
        return ROCK
    elif instr in ("B", "Y"):
        return PAPER
    elif instr in ("C", "Z"):
        return SCISSORS
    else:
        raise Exception(f"Unknown instruction: {instr}.")


def process_input(_input: List[str]) -> List[Tuple[int, int]]:
    strategy = []

    for line in _input:
        opp, you = line.split(" ")

        opp = decode_instruction(opp)
        you = decode_instruction(you)

        strategy.append((opp, you))

    return strategy


def part_1(opp: int, you: int) -> int:
    if you == opp:
        return DRAW + you
    elif you == WINS_AGAINST[opp]:
        return LOSS + you
    elif you == LOSES_TO[opp]:
        return WIN + you
    else:
        raise Exception(f"Unknown instruction: {you}.")


def part_2(opp: int, you: int) -> int:
    if you == ROCK:
        return LOSS + WINS_AGAINST[opp]
    elif you == PAPER:
        return DRAW + opp
    elif you == SCISSORS:
        return WIN + LOSES_TO[opp]
    else:
        raise Exception(f"Unknown instruction: {you}.")


@timer
def main(filename: str) -> Tuple[int, int]:
    _input = read_input(filename)
    strategy = process_input(_input)
    part_1_score = sum([part_1(*v) for v in strategy])
    part_2_score = sum([part_2(*v) for v in strategy])
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc2.txt")
    print(f"PART 1: {part_1_score}")  # 12740
    print(f"PART 2: {part_2_score}")  # 11980
