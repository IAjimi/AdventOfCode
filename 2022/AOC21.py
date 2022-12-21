from typing import List, Tuple, Set
import parse
from _utils import read_input, timer, Solution


def process_input(filename: str):
    _input = read_input(filename)
    known = {}
    queue = []
    for line in _input:
        if "+" in line:
            parsed_line = parse.parse("{monkey1}: {dep1} + {dep2}", line)
            queue.append(
                (parsed_line["monkey1"], "+", parsed_line["dep1"], parsed_line["dep2"])
            )
        elif "-" in line:
            parsed_line = parse.parse("{monkey1}: {dep1} - {dep2}", line)
            queue.append(
                (parsed_line["monkey1"], "-", parsed_line["dep1"], parsed_line["dep2"])
            )
        elif "*" in line:
            parsed_line = parse.parse("{monkey1}: {dep1} * {dep2}", line)
            queue.append(
                (parsed_line["monkey1"], "*", parsed_line["dep1"], parsed_line["dep2"])
            )
        elif "/" in line:
            parsed_line = parse.parse("{monkey1}: {dep1} / {dep2}", line)
            queue.append(
                (parsed_line["monkey1"], "/", parsed_line["dep1"], parsed_line["dep2"])
            )
        else:
            parsed_line = parse.parse("{monkey1}: {:d}", line)
            known[parsed_line["monkey1"]] = parsed_line.fixed[0]

    return queue, known


def process_monkeys(queue, known):
    while queue:
        monkey, op, dep1, dep2 = queue.pop(
            0
        )  # need to pop at front bc appending at back
        if dep1 in known and dep2 in known:
            n1, n2 = known[dep1], known[dep2]
            known[monkey] = eval(f"{n1} {op} {n2}")
            if monkey == "root":
                return known[monkey]
        else:
            queue.append((monkey, op, dep1, dep2))

    return 0


@timer
def main(filename: str) -> Solution:
    queue, known = process_input(filename)
    part_1_solution = process_monkeys(queue, known)
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc21.txt")
    print(f"PART 1: {part_1_solution}")  # 145167969204648
    print(f"PART 2: {part_2_solution}")  #
