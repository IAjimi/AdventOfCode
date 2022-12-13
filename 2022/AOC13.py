from typing import List, Tuple, Set

from _utils import read_input, timer, Solution, product


def process_input(filename: str):
    _input = read_input(filename)
    _input = [eval(l) for l in _input if l != ""]
    return _input


def compare_pairs(pair1, pair2) -> bool:
    if type(pair1) == int and type(pair2) == int:
        if pair1 < pair2:
            return True
        elif pair1 > pair2:
            return False
        else:
            return None

    i = 0
    while i < len(pair1) and i < len(pair2):
        p1, p2 = pair1[i], pair2[i]
        if type(p1) == int and type(p2) == int:
            if p1 < p2:
                return True
            elif p1 > p2:
                return False
            else:
                comp = None
        elif type(p1) == list and type(p2) == int:
            comp = compare_pairs(p1, [p2])
        elif type(p1) == int and type(p2) == list:
            comp = compare_pairs([p1], p2)
        else:
            comp = compare_pairs(p1, p2)

        if comp is not None:
            return comp
        else:
            i += 1

    if len(pair1) < len(pair2):
        return True
    elif len(pair1) > len(pair2):
        return False
    else:
        return None


def part1(_input) -> int:
    _input = [compare_pairs(_input[i], _input[i + 1]) for i in range(0, len(_input), 2)]
    return sum([1 + i if pair else 0 for i, pair in enumerate(_input)])


class InsertionSort:
    def insert(self, A: List[int], i: int) -> List[int]:
        j = i - 1

        while j >= 0 and compare_pairs(A[i], A[j]):
            A = self.swap(A, i, j)
            i -= 1
            j -= 1

        return A

    def swap(self, A: List[int], i: int, j: int) -> List[int]:
        A[i], A[j] = A[j], A[i]
        return A

    def sort(self, A: List[int]) -> List[int]:
        for i in range(len(A)):
            A = self.insert(A, i)

        return A


def part2(_input) -> int:
    _input.append([[2]])
    _input.append([[6]])
    _input = InsertionSort().sort(_input)
    return product([i + 1 for i, v in enumerate(_input) if v in ([[2]], [[6]])])


@timer
def main(filename: str) -> Solution:
    _input = process_input(filename)
    part_1_solution = part1(_input)
    part_2_solution = part2(_input)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc13.txt")
    print(f"PART 1: {part_1_solution}")  # 5185
    print(f"PART 2: {part_2_solution}")  # 23751
