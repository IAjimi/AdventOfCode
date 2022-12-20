from typing import List

from _utils import read_input, timer, Solution

DECRYPTION_KEY = 811589153


class Node:
    def __init__(self, val: int, prev: "Node" = None, next: "Node" = None):
        self.val = val
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"Node({self.val}, prev={self.prev.val}, next={self.next.val})"


def process_input(filename: str, decrypt_key: bool) -> List[Node]:
    _input = read_input(filename)
    if decrypt_key:
        _input = [Node(int(val) * DECRYPTION_KEY) for val in _input]
    else:
        _input = [Node(int(val)) for val in _input]

    for i, node in enumerate(_input):
        _input[i].prev = _input[(i - 1) % len(_input)]
        _input[i].next = _input[(i + 1) % len(_input)]
    return _input


def mix_file(_input: List[Node]) -> List[Node]:
    n_nodes = len(_input)

    for i in range(n_nodes):
        node = _input[i]
        if node.val == 0:
            continue

        node.prev.next, node.next.prev = node.next, node.prev  # remove node
        new_prev_node, new_next_node = node.prev, node.next

        move = node.val % (n_nodes - 1)
        for _ in range(move):
            new_prev_node = new_prev_node.next
            new_next_node = new_next_node.next

        node.prev, node.next = new_prev_node, new_next_node  # update node pointers
        new_prev_node.next, new_next_node.prev = node, node
    return _input


def grove_coordinates(nodes: List[Node]) -> int:
    node = nodes[0]
    while node.val != 0:
        node = node.next

    solution = 0
    for i in range(3_000 + 1):
        if i in (1_000, 2_000, 3_000):
            solution += node.val
        node = node.next

    return solution


def part1(filename: str) -> int:
    nodes = process_input(filename, decrypt_key=False)
    nodes = mix_file(nodes)
    return grove_coordinates(nodes)


def part2(filename: str) -> int:
    nodes = process_input(filename, decrypt_key=True)
    for i in range(10):
        nodes = mix_file(nodes)
    return grove_coordinates(nodes)


@timer
def main(filename: str) -> Solution:
    part_1_solution = part1(filename)
    part_2_solution = part2(filename)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc20.txt")
    print(f"PART 1: {part_1_solution}")  # 19070
    print(f"PART 2: {part_2_solution}")  # 14773357352059
