from typing import List, Tuple, Set

from _utils import read_input, timer, Solution


class Node:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.size = 0

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def add_file(self, file_size: int) -> None:
        """
        Add file to current dir and parents.
        """
        queue = [self]
        while queue:
            node = queue.pop()
            node.size += file_size
            if node.parent:
                queue.append(node.parent)

    def __repr__(self):
        return f"Node('{self.name}', {self.size})"


def process_input(_input: List[str]) -> Tuple[Node, Set[Node]]:
    root_dir = Node("/")
    tree = {root_dir}  # need smthg to hold refs of nodes
    current_dir = root_dir

    for line in _input:
        commands = line.split(" ")
        if commands[0] == "$" and commands[1] == "cd":
            new_dir = commands[2]

            if new_dir == "..":
                current_dir = (
                    current_dir.parent if current_dir != root_dir else root_dir
                )
            else:
                new_dir = Node(new_dir, current_dir)
                current_dir = new_dir
                tree.add(new_dir)
        elif commands[0] == "$" and commands[1] == "ls":
            continue
        elif commands[0] == "dir":
            child = Node(commands[1], current_dir)
            current_dir.add_child(child)
            tree.add(child)
        else:
            current_dir.add_file(int(commands[0]))

    return root_dir, tree


def part_2(root_dir: Node, tree: Set[Node]) -> int:
    """
    Find smallest directory to delete to have 30_000_000
    unusued space.
    """
    total_space, unused_space = 70_000_000, 30_000_000
    currently_unusued = total_space - root_dir.size
    need_to_del = unused_space - currently_unusued

    min_size = total_space
    for n in tree:
        if n.size >= need_to_del:
            min_size = min(n.size, min_size)

    return min_size


@timer
def main(filename: str) -> Solution:
    _input = read_input(filename)
    root_dir, tree = process_input(_input)
    part_1_solution = sum([n.size for n in tree if n.size <= 100_000])
    part_2_solution = part_2(root_dir, tree)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc7.txt")
    print(f"PART 1: {part_1_solution}")  # 1307902
    print(f"PART 2: {part_2_solution}")  # 7068748
