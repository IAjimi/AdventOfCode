from typing import List, Tuple, Set

from _utils import read_input, timer, Solution


def process_input(filename: str):
    _input = read_input(filename)
    _input = [line for line in _input if line != ""]
    monkeys = [Monkey(*_input[i : i + 6]) for i in range(0, len(_input), 6)]
    return monkeys


class Monkey:
    def __init__(self, monkey_id, items, operation_str, test_val, monkey1, monkey2):
        self._id = int(monkey_id.replace("Monkey ", "").replace(":", ""))
        items = items.replace("Starting items: ", "").strip()
        self.items = list(map(int, items.split(",")))
        self.operation = self.parse_operation(operation_str)
        self.test_val = int(test_val.replace("Test: divisible by", "").strip())
        self.monkey1 = int(monkey1.replace("If true: throw to monkey", "").strip())
        self.monkey2 = int(monkey2.replace("If false: throw to monkey", "").strip())
        self.items_inspected = 0

    def __repr__(self):
        return f"Monkey({self._id}, {self.items})"

    def parse_operation(self, operation_str: str):
        if "old * old" in operation_str:
            return lambda x: x ** 2
        elif "*" in operation_str:
            operation_val = operation_str.replace("Operation: new = old *", "").strip()
            return lambda x: x * int(operation_val)
        else:
            operation_val = operation_str.replace("Operation: new = old +", "").strip()
            return lambda x: x + int(operation_val)

    def test_object(self, worry_level: int) -> int:
        return self.monkey1 if worry_level % self.test_val == 0 else self.monkey2

    def take_turns(self):
        item_moves = []

        for worry_level in self.items:
            new_worry_level = self.operation(worry_level) // 3
            item_recipient = self.test_object(new_worry_level)
            item_moves.append((item_recipient, new_worry_level))

        self.items_inspected += len(self.items)

        return item_moves


def simulate(monkeys, n_rounds):
    items_inspected = [0 for m in monkeys]

    for r in range(n_rounds):
        for m in monkeys:
            items_inspected[m._id] += len(m.items)
            item_moves = m.take_turns()
            m.items = []
            for monkey_id, worry_level in item_moves:
                monkeys[monkey_id].items.append(worry_level)

    items_inspected.sort()
    print(items_inspected)
    return items_inspected[-1] * items_inspected[-2]


@timer
def main(filename: str) -> Solution:
    monkeys = process_input(filename)
    part_1_solution = simulate(monkeys, n_rounds=20)
    part_2_solution = 0  # simulate(monkeys, n_rounds=1000)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc11.txt")
    print(f"PART 1: {part_1_solution}")  # 64032
    print(f"PART 2: {part_2_solution}")  #
