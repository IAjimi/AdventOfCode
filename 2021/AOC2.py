from _utils import read_input, timer


def parse_instructions(full_instruction_str: str):
    """
    Parse a string and return a tuple of ints.
    In part 1, the tuple represents (horizontal pos change, depth change).
    In part 2, the tuple represents (special forward value change, aim change).
    """
    instruction, value = full_instruction_str.split(" ")
    value = int(value)

    if "forward" in instruction:
        return value, 0
    elif "down" in instruction:
        return 0, value
    elif "up" in instruction:
        return 0, -value
    else:
        raise Exception("Unrecognized instruction.")


def process_input(filepath: str):
    """
    Open and read file at filepath, return list of tuples.
    """
    _input = read_input(filepath)
    return [parse_instructions(i) for i in _input]


def part_1(_input: list):
    horizontal_change, depth_change = zip(
        *_input
    )  # unzip input into x changes and y changes
    return sum(horizontal_change) * sum(depth_change)


def part_2(_input: list):
    """
    Because of the way the _input tuple is constructed,
    tuples with x,0 correspond to 'forward' instructions
    and tuples with 0,y correspond to 'up/down' instructions.
    """
    hor_pos, depth, aim = 0, 0, 0

    for forward_value, aim_change in _input:
        if aim_change != 0:
            aim += aim_change
        else:
            hor_pos += forward_value
            depth += aim * forward_value

    return hor_pos * depth


@timer
def main(filename: str):
    _input = process_input(filename)
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc2.txt")
    print(f"PART 1: {part_1_score}")  # 1746616
    print(f"PART 2: {part_2_score}")  # 1741971043