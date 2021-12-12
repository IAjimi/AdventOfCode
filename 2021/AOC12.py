"""
Part 1 completed at 00:25:50, rank 2233.
Part 2 completed at 00:32:24, rank 1384.

Both handled with BFS.

Code still needs to be cleaned up and optimized - runs in 0.64s
for both parts (slowest AOC solution yet) after 1st cleanup.
"""

from collections import defaultdict
from _utils import read_input, timer

START = "start"
END = "end"


def parse_input(_input: list):
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


def part_1(connections: dict):
    """
    Counts the number of unique paths that connect the
    start to the end. Nodes with uppercase names can be
    visited as much as needed. Nodes with lowercase names can
    only be visited once.
    """
    queue = [(START, set())]
    valid_paths_counter = 0

    while queue:
        current_node, visited = queue.pop()

        if current_node == END:
            valid_paths_counter += 1
        elif current_node.isupper() or current_node not in visited:
            visited.add(current_node)
            next_nodes = connections[current_node]

            for node in next_nodes:
                queue.append((node, visited.copy()))

    return valid_paths_counter


def part_2(connections: dict):
    """
    Same as part 1, except a single small cave (lowercase name, not "start"
    or "end") can be visited twice. This is handled with a boolean passed on
    to the queue.
    """
    queue = [(START, set(), False)]
    valid_paths_counter = 0

    while queue:
        current_node, visited, small_twice = queue.pop()

        if current_node == END:
            valid_paths_counter += 1
        # Big cave or unvisited small cave
        elif current_node.isupper() or current_node not in visited:
            next_nodes = connections[current_node]
            visited.add(current_node)

            for node in next_nodes:
                queue.append((node, visited.copy(), small_twice))
        # 1st small cave to be visited 2x
        elif (
            current_node.islower()
            and current_node not in {START, END}
            and not small_twice
        ):
            next_nodes = connections[current_node]
            small_twice = True

            for node in next_nodes:
                queue.append((node, visited.copy(), small_twice))

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
