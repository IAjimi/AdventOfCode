from typing import List, Tuple, Set
import parse
from _utils import read_input, timer, Solution

ROOT = "root"


def process_input(filename: str, part1: bool):
    _input = read_input(filename)
    known = {}
    queue = []
    for line in _input:
        if any(c.isdigit() for c in line):
            parsed_line = parse.parse("{monkey1}: {:d}", line)
            known[parsed_line["monkey1"]] = parsed_line.fixed[0]
        else:
            parsed_line = parse.parse("{monkey1}: {dep1} {op} {dep2}", line)
            if parsed_line["monkey1"] == ROOT and not part1:
                op = "-"
            else:
                op = parsed_line["op"]
            queue.append(
                (
                    parsed_line["monkey1"],
                    op,
                    parsed_line["dep1"],
                    parsed_line["dep2"],
                )
            )
    return queue, known


def process_monkeys(queue, known) -> int:
    while queue:
        monkey, op, dep1, dep2 = queue.pop(
            0
        )  # need to pop at front bc appending at back
        if dep1 in known and dep2 in known:
            n1, n2 = known[dep1], known[dep2]
            known[monkey] = eval(f"{n1} {op} {n2}")
            if monkey == ROOT:
                return known[monkey]
        else:
            queue.append((monkey, op, dep1, dep2))

    return 0


def get_guess_result(filename: str, guess: int) -> int:
    queue, known = process_input(filename, part1=False)
    known["humn"] = guess
    return process_monkeys(queue, known)


def binary_search(filename: str, target: int = 0) -> int:
    left = get_guess_result(filename, 0)
    right = get_guess_result(filename, 10_000_000_000_000)

    while True:
        mid = (left + right) // 2
        res = get_guess_result(filename, mid)

        if res == target:
            return mid
        elif res < target:
            left = mid + 1
        else:
            right = mid - 1


@timer
def main(filename: str) -> Solution:
    # TODO manually changed input so that root is - numbers
    queue, known = process_input(filename, part1=True)
    part_1_solution = process_monkeys(queue, known)
    part_2_solution = binary_search(filename, target=0)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc21.txt")
    print(f"PART 1: {part_1_solution}")  # 145167969204648
    print(f"PART 2: {part_2_solution}")  # 3330805295850
