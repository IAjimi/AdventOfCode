"""
Thought iterating over the whole board to check that the number is there would
be slow so tried to use different data structure to speed that check + verifying
whether a board is complete or not. Runs in about 0.009 seconds locally.
"""


from _utils import read_input, timer

import re


def parse_input(_input: list):
    """
    Returns data structures used to solve the puzzle.

    :param: _input: list[str], original input

    :return:
        bingo_numbers: ordered list of bingo numbers

        board: dict representing the board. Keys are unique board ID, values
        is another dict where keys are bingo numbers and values the position
        of the numbers within the board. Aim is to give O(1) access to the
        position of specific numbers within a board later on.

        bingo_grid: dict representing the board and 'found' numbers.
        Keys are unique board ID, value is a matrix representing whether a
        number was found in the current position or not.
    """
    bingo_numbers = [int(i) for i in _input[0].split(",")]

    all_boards = {}
    bingo_grid = {}
    raw_board = [re.sub("\s+", " ", line).strip() for line in _input[1:] if line != ""]

    for ix in range(5, len(raw_board) + 1, 5):  # board is 5x5
        all_boards[ix] = {}
        bingo_grid[ix] = [[0, 0, 0, 0, 0] for i in raw_board[ix : ix + 5]]

        # Parse board as list[list[int]] at first, then use to create dict
        current_board = [list(map(int, i.split())) for i in raw_board[ix : ix + 5]]

        for i in range(len(current_board)):
            for j in range(len(current_board[i])):
                number = current_board[i][j]
                all_boards[ix][number] = i, j

    return bingo_numbers, all_boards, bingo_grid


def get_bingo_score(all_boards: dict, board_number: int, bingo_numbers: list, ix: int):
    winning_sum = sum(
        [k for k in all_boards[board_number].keys() if k not in bingo_numbers[: ix + 1]]
    )
    return bingo_numbers[ix] * winning_sum


def play_bingo(bingo_numbers: list, all_boards: dict, bingo_grid: dict):
    """
    Returns part 1 score (score from 1st completed board) and part 2 score
    (score from last completed score).
    """
    won = set()  # set for fast membership checks in while loop

    for ix, bingo_num in enumerate(bingo_numbers):
        # for every board
        for board_number in all_boards:
            # if number in board & board not 'won' yet, update grid
            if bingo_num in all_boards[board_number] and board_number not in won:
                x, y = all_boards[board_number][bingo_num]
                bingo_grid[board_number][x][y] = 1

                # check this is now a sum
                hor_check = [bingo_grid[board_number][x][n] for n in range(5)]
                vert_check = [bingo_grid[board_number][n][y] for n in range(5)]

                if sum(hor_check) == 5 or sum(vert_check) == 5:
                    won.add(board_number)
                    if len(won) == 1:
                        part_1_score = get_bingo_score(
                            all_boards, board_number, bingo_numbers, ix
                        )

                    # last score will be returned by func - better way to do this?
                    part_2_score = get_bingo_score(
                        all_boards, board_number, bingo_numbers, ix
                    )

    return part_1_score, part_2_score


@timer
def main(filepath: str):
    """
    Returns solution for AOC day 4 from filepath.
    """
    _input = read_input(filepath)
    bingo_numbers, all_boards, bingo_grid = parse_input(_input)
    part_1_score, part_2_score = play_bingo(bingo_numbers, all_boards, bingo_grid)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc4.txt")
    print(f"PART 1: {part_1_score}")  # 87456
    print(f"PART 2: {part_2_score}")  # 15561
