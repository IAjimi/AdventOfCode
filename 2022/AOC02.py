from typing import Tuple, List

from _utils import read_input, timer


ROCK = 1
PAPER = 2
SCISSORS = 3

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
    if opp == you:
        return DRAW + you
    elif opp == ROCK and you == SCISSORS:
        return LOSS + you
    elif opp == SCISSORS and you == PAPER:
        return LOSS + you
    elif opp == PAPER and you == ROCK:
        return LOSS + you
    elif you == ROCK and opp == SCISSORS:
        return WIN + you
    elif you == SCISSORS and opp == PAPER:
        return WIN + you
    elif you == PAPER and opp == ROCK:
        return WIN + you
    else:
        raise Exception


def part_2(opp: int, you: int) -> int:
    # need to lose
    if opp == ROCK and you == ROCK:
        return LOSS + SCISSORS
    elif opp == SCISSORS and you == ROCK:
        return LOSS + PAPER
    elif opp == PAPER and you == ROCK:
        return LOSS + ROCK
    # need to draw
    elif you == PAPER:
        return DRAW + opp
    # need to win
    elif opp == ROCK and you == SCISSORS:
        return WIN + PAPER
    elif opp == SCISSORS and you == SCISSORS:
        return WIN + ROCK
    elif opp == PAPER and you == SCISSORS:
        return WIN + SCISSORS
    else:
        raise Exception


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
