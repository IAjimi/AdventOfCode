"""
Part 1 completed at 00:25:50, rank 2233.
Part 2 completed at 00:32:24, rank 1384.

Both handled with BFS.

Code still needs to be cleaned up and optimized - runs in 0.83s
for both parts (slowest AOC solution yet).
"""

from collections import defaultdict
from _utils import read_input, timer


def parse_input(_input):
    """
    Return dictionary, with key as node name and value the list
    of nodes that can be reached through the key node.
    """
    connections = defaultdict(list)
    for line in _input:
        _from, _to = line.split("-")
        connections[_from].append(_to)
        connections[_to].append(_from)
    return connections


def part_1(connections):
    """
    Counts the number of unique paths that connect the
    start to the end. Nodes with uppercase names can be
    visited as much as needed. Nodes with lowercase names can
    only be visited once.
    """
    queue = [("start", [])]
    valid_paths_counter = 0

    while queue:
        current_node, visited = queue.pop()

        if current_node == "end":
            valid_paths_counter += 1
        elif current_node.isupper() or current_node not in set(visited):
            next_nodes = connections[current_node]

            for node in next_nodes:
                queue.append((node, visited.copy() + [current_node]))

    return valid_paths_counter


def part_2(connections):
    """
    Same as part 1, except a single small cave (lowercase name, not "start"
    or "end") can be visited twice. This is handled with a boolean passed on
    to the queue.
    """
    queue = [("start", [], False)]
    valid_paths_counter = 0

    while queue:
        current_node, visited, small_twice = queue.pop()

        if current_node == "end":
            valid_paths_counter += 1

        elif current_node.isupper() or current_node not in set(visited):
            next_nodes = connections[current_node]

            for node in next_nodes:
                queue.append((node, visited.copy() + [current_node], small_twice))

        elif (
            current_node.islower()
            and current_node not in {"start", "end"}
            and not small_twice
        ):
            next_nodes = connections[current_node]

            for node in next_nodes:
                queue.append((node, visited.copy() + [current_node], True))

    return valid_paths_counter


@timer
def main(filepath: str):
    _input = read_input(filepath)
    connections = parse_input(_input)
    part_1_score = part_1(connections)
    part_2_score = part_2(connections)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc12.txt")
    print(f"PART 1: {part_1_score}")  # 3485
    print(f"PART 2: {part_2_score}")  # 85062
