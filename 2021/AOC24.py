from typing import Tuple, List, Set

from _utils import read_input, timer


class Programs:
    def __init__(
        self,
        filepath: str = None,
        instr_list: List[str] = None,
        input_list: List[int] = None,
    ):
        VARIABLES = {"w", "x", "y", "z"}
        self.registers = {var_name: 0 for var_name in VARIABLES}

        if filepath:
            self.instr_list = read_input(filepath)
        elif not filepath and instr_list:
            self.instr_list = instr_list
        else:
            raise Exception("No instructions provided.")

        self.input = input_list
        self.i = 0

    def run(self):
        for instr_str in self.instr_list:
            command = instr_str[:3]
            values = instr_str[4:]

            if command == "inp":
                self.inp(values)
            elif command == "add":
                self.add(values)
            elif command == "mul":
                self.mul(values)
            elif command == "div":
                self.div(values)
            elif command == "mod":
                self.mod(values)
            elif command == "eql":
                self.eql(values)
            else:
                raise Exception("Unknown instruction.")

        return self.registers

    def get_val(self, x):
        try:
            return int(x)
        except:
            return self.registers[x]

    # def read_values(self, values):
    #     a, b = values.split(" ")
    #     return self.get_val(a), self.get_val(b)

    def inp(self, values: str):
        var_name = values.strip()
        self.registers[var_name] = self.input[self.i]
        self.i += 1

    def add(self, values):
        a, b = values.split(" ")
        self.registers[a] = self.get_val(a) + self.get_val(b)

    def mul(self, values):
        a, b = values.split(" ")
        self.registers[a] = self.get_val(a) * self.get_val(b)

    def div(self, values):
        a, b = values.split(" ")
        if self.get_val(b) != 0:
            self.registers[a] = self.get_val(a) // self.get_val(b)
        else:
            raise Exception("Division by 0 not allowed.")

    def mod(self, values):
        a, b = values.split(" ")
        self.registers[a] = self.get_val(a) % self.get_val(b)

    def eql(self, values):
        a, b = values.split(" ")
        self.registers[a] = 1 if self.get_val(a) == self.get_val(b) else 0


@timer
def main(filepath: str) -> Tuple[int, int]:
    """
    Returns part 1 & 2 scores from a filepath.

    Program class needs to be fed a 14 digit number,
    with no 0 digits, until register z == 0.
    """
    model_number_int = 99999999999999

    while True:
        if model_number_int % 10000 == 0:
            print(f"running {model_number_str}")

        model_number_str = str(model_number_int)

        if "0" in model_number_str:
            model_number_int += -1
        else:
            model_number_list = [int(r) for r in model_number_str]
            registers = Programs(
                filepath=filepath, input_list=model_number_list
            ).run()
            if registers["z"] == 0:
                break
            else:
                model_number_int += -1

    part_1_score = model_number_str
    part_2_score = 0

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc24.txt")
    print(f"PART 1: {part_1_score}")  # .
    print(f"PART 2: {part_2_score}")  # .
