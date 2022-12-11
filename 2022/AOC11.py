from copy import deepcopy
from typing import List, Tuple
import parse

from _utils import read_input, timer, Solution, product


class Monkey:
    def __init__(
        self,
        monkey_id: str,
        items: str,
        operation: str,
        test_val: str,
        monkey1: str,
        monkey2: str,
    ):
        self._id = parse.parse("Monkey {:d}:", monkey_id)[0]
        self.items = list(map(int, items.replace("Starting items: ", "").split(",")))
        self.operation = self.parse_operation(operation)
        self.test_val = parse.parse("Test: divisible by {:d}", test_val)[0]
        self.monkey1 = parse.parse("If true: throw to monkey {:d}", monkey1)[0]
        self.monkey2 = parse.parse("If false: throw to monkey {:d}", monkey2)[0]
        self.items_inspected = 0

    def __repr__(self):
        return f"Monkey({self._id}, {self.items})"

    def parse_operation(self, operation_str: str):
        if "old * old" in operation_str:
            return lambda x: x ** 2
        elif "*" in operation_str:
            operation_val = parse.parse("Operation: new = old * {:d}", operation_str)[0]
            return lambda x: x * operation_val
        elif "+" in operation_str:
            operation_val = parse.parse("Operation: new = old + {:d}", operation_str)[0]
            return lambda x: x + operation_val
        else:
            raise NotImplementedError

    def test_object(self, worry_level: int) -> int:
        return self.monkey1 if worry_level % self.test_val == 0 else self.monkey2

    def inspect_object(self, modulo: int, part1: bool) -> Tuple[int, int]:
        worry_level = self.operation(self.items.pop()) % modulo
        if part1:
            worry_level = worry_level // 3
        item_recipient = self.test_object(worry_level)
        return item_recipient, worry_level

    def take_turn(self, modulo: int, part1: bool) -> List[Tuple[int, int]]:
        item_moves = []
        self.items_inspected += len(self.items)

        while self.items:
            item_recipient, worry_level = self.inspect_object(modulo, part1)
            item_moves.append((item_recipient, worry_level))

        return item_moves


def process_input(filename: str) -> List[Monkey]:
    _input = read_input(filename)
    _input = [line.strip() for line in _input if line != ""]
    monkeys = [Monkey(*_input[i : i + 6]) for i in range(0, len(_input), 6)]
    return monkeys


def simulate(monkeys: List[Monkey], part1: bool) -> int:
    modulo = product([m.test_val for m in monkeys])
    n_rounds = 20 if part1 else 10_000

    for r in range(n_rounds):
        for m in monkeys:
            item_moves = m.take_turn(modulo, part1)
            for monkey_id, worry_level in item_moves:
                monkeys[monkey_id].items.append(worry_level)

    first, second, *_ = sorted([m.items_inspected for m in monkeys], reverse=True)
    return first * second


@timer
def main(filename: str) -> Solution:
    monkeys = process_input(filename)
    part_1_solution = simulate(deepcopy(monkeys), part1=True)
    part_2_solution = simulate(monkeys, part1=False)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc11.txt")
    print(f"PART 1: {part_1_solution}")  # 64032
    print(f"PART 2: {part_2_solution}")  # 12729522272
