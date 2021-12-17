"""
Part 1 completed at 00:25:50, rank 2233.
Part 2 completed at 00:32:24, rank 1384.

Both handled with BFS.
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


def count_unique_paths(connections: dict, part_2: bool):
    """
    Counts the number of unique paths that connect the
    start to the end. Nodes with uppercase names can be
    visited as much as needed.

    In part 1, nodes with lowercase names can only be visited once.
    In part 2, a single small cave (lowercase name, not "start" or "end")
    can be visited twice. This is handled by keeping track of a boolean passed on
    to the queue.
    """
    queue = [(START, set(), False)]
    valid_paths_counter = 0

    while queue:
        current_node, small_visited, small_twice = queue.pop()

        # Reached end
        if current_node == END:
            next_nodes = []
            valid_paths_counter += 1
        # Reached big cave
        elif current_node.isupper():
            next_nodes = connections[current_node]
        # Reached unvisited small cave
        elif current_node not in small_visited:
            next_nodes = connections[current_node]
            small_visited.add(current_node)
        # If in part 2, reach 1st small cave to be visited 2x
        elif part_2 and current_node != START and not small_twice:
            next_nodes = connections[current_node]
            small_twice = True
        # Reached dead end (e.g., visited small cave)
        else:
            next_nodes = []

        for node in next_nodes:
            queue.append((node, small_visited.copy(), small_twice))

    return valid_paths_counter


@timer
def main(filepath: str):
    _input = read_input(filepath)
    connections = parse_input(_input)
    part_1_score = count_unique_paths(connections, part_2=False)
    part_2_score = count_unique_paths(connections, part_2=True)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc12.txt")
    print(f"PART 1: {part_1_score}")  # 3485
    print(f"PART 2: {part_2_score}")  # 85062
