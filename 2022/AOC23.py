from collections import defaultdict
from typing import List, Tuple, Set

from _utils import read_input, timer, Solution, Point

S, N, W, E = (0, 1), (0, -1), (-1, 0), (1, 0)
NE, NW = (1, -1), (-1, -1)
SE, SW = (1, 1), (-1, 1)
MOVES = (N, S, W, E)


def process_input(filename: str):
    _input = read_input(filename)
    elves = set()
    for y, line in enumerate(_input):
        for x, char in enumerate(line):
            if char == "#":
                elves.add((x, y))
    return elves


def get_neighbors(elves, pos):
    x, y = pos
    pos_dict = {"S": S, "N": N, "W": W, "E": E, "NE": NE, "NW": NW, "SE": SE, "SW": SW}
    neighbors = {}
    for pos_name, (dx, dy) in pos_dict.items():
        neighbors[pos_name] = (x + dx, y + dy) in elves
    return neighbors


def play_round(elves, move_ix):
    no_move = True
    moves = defaultdict(list)
    new_elves = set()
    for elf in elves:
        new_elves.add(elf)
        neighs = get_neighbors(elves, elf)

        # if no neighbors, stay put
        if not any(neighs.values()):
            continue

        # else propose move
        x, y = elf
        checks = [
            not neighs["N"] and not neighs["NE"] and not neighs["NW"],
            not neighs["S"] and not neighs["SE"] and not neighs["SW"],
            not neighs["W"] and not neighs["NW"] and not neighs["SW"],
            not neighs["E"] and not neighs["NE"] and not neighs["SE"],
        ]

        for i in range(4):
            if checks[(move_ix + i) % 4]:
                dx, dy = MOVES[(move_ix + i) % 4]
                moves[(x + dx, y + dy)].append((x, y))
                break

    for new_pos, old_pos in moves.items():
        # actually move
        if len(old_pos) == 1:
            new_elves.add(new_pos)
            new_elves.remove(old_pos[0])
            no_move = False

    return new_elves, no_move


def simulate(elves, rounds: int):
    move_ix = 0
    for r in range(rounds):
        elves, no_move = play_round(elves, move_ix)
        if no_move:
            return r + 1
        move_ix += 1

    min_x = min(x for x, _ in elves)
    max_x = max(x for x, _ in elves)
    min_y = min(y for _, y in elves)
    max_y = max(y for _, y in elves)
    return (1 + max_x - min_x) * (1 + max_y - min_y) - len(elves)


@timer
def main(filename: str) -> Solution:
    elves = process_input(filename)
    part_1_solution = simulate(elves, rounds=10)
    part_2_solution = simulate(elves, rounds=1000)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc23.txt")
    print(f"PART 1: {part_1_solution}")  # 3871
    print(f"PART 2: {part_2_solution}")  # 925
