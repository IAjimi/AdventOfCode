"""
Slower to do than previous days because required more involved logic, especially in part 2.
"""


from _utils import read_input, timer


def part_1(_input: list):
    """
    Returns the number of signals that are of length 2, 3, 4, or 7
    (i.e., lengths that allow us to immediately map a signal to a digit).
    """
    output_lines = [i.split(" | ")[1] for i in _input]
    output_lines_len = [
        1 for line in output_lines for i in line.split(" ") if len(i) in {2, 3, 4, 7}
    ]
    part_1_score = sum(output_lines_len)
    return part_1_score


def deduce_signals(full_line: list):
    potential = {}

    # First, start with the signals we can immediately attribute to a number (unique length)
    for signal in full_line:
        signal = set(signal)

        if len(signal) == 2:
            potential[1] = signal
        elif len(signal) == 3:
            potential[7] = signal
        elif len(signal) == 4:
            potential[4] = signal
        elif len(signal) == 7:
            potential[8] = signal

    # Then move on to signals with more involved logic
    for signal in full_line:
        signal = set(signal)
        if len(signal) == 5:
            if len(potential[4].difference(signal)) == 2:
                potential[2] = signal
            elif len(potential[1].difference(signal)) == 1:
                potential[5] = signal
            elif len(potential[1].difference(signal)) == 0:
                potential[3] = signal
            else:
                raise Exception("Missing logic to detect len 5 signal code.")
        elif len(signal) == 6:
            if len(potential[1].difference(signal)) == 1:
                potential[6] = signal
            elif len(potential[4].difference(signal)) == 1:
                potential[0] = signal
            elif len(potential[4].difference(signal)) == 0:
                potential[9] = signal
            else:
                raise Exception("Missing logic to detect len 6 signal code.")

    return potential


def get_decoder(potential: dict):
    """
    Returns a dictionary that maps signal patterns to digits.
    Needs sorting so we can match with output.
    """
    decoder = {}
    for k, v in potential.items():
        if v:
            v_lst = list(v)
            v_lst.sort()
            decoder["".join(v_lst)] = k
    return decoder


def get_output_code(line: str):
    full_line = line.replace(" | ", " ").split(" ")
    potential = deduce_signals(full_line)  # get int -> set(str)
    decoder = get_decoder(potential)  # get str -> int

    output_list = line.split(" | ")[1].split(" ")
    output_list = [
        "".join(sorted(s)) for s in output_list
    ]  # sort it so can be used as decoder key
    output_code = [str(decoder[segment]) for segment in output_list]
    return int("".join(output_code))


def part_2(_input):
    part_2_score = [get_output_code(line) for line in _input]
    return sum(part_2_score)


@timer
def main(filepath: str):
    _input = read_input(filepath)
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc8.txt")
    print(f"PART 1: {part_1_score}")  # 488
    print(f"PART 2: {part_2_score}")  # 1040429
