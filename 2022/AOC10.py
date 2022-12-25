from typing import List

from _utils import read_input, timer, Solution


def process_instructions(_input: List[str]) -> List[int]:
    X = [1]

    for line in _input:
        X.append(X[-1])

        if line.startswith("addx"):
            _, val = line.split(" ")
            X.append(X[-1] + int(val))

    return X


def produce_image(X: List[int]) -> str:
    image = ""
    for i in range(0, 240, 40):
        row = [
            "#" if x - 1 <= cycle <= x + 1 else "."
            for cycle, x in enumerate(X[i : i + 40])
        ]
        image += " ".join(row)
        image += "\n"
    return image


@timer
def main(filename: str) -> Solution:
    _input = read_input(filename)
    X = process_instructions(_input)
    part_1_solution = sum([X[i - 1] * i for i in range(20, 220 + 1, 40)])
    part_2_solution = produce_image(X)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc10.txt")
    print(f"PART 1: {part_1_solution}")  # 12880
    print(f"PART 2: \n {part_2_solution}")  # FCJAPJRE
