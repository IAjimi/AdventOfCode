"""
Needs serious cleaning. Slower to do than previous days because required
more involved logic, especially in part 2.
"""


from _utils import read_input, timer

def part_1(_input:list):
    output_lines = [i.split(' | ')[1] for i in _input]
    output_lines_len = [[len(i) for i in line.split(' ')] for line in output_lines]
    output_lines_len = [i for sublist in output_lines_len for i in sublist]
    part_1_score = len([i for i in output_lines_len if i in {2, 3, 4, 7}])
    return part_1_score

def get_decoder(potential:dict):
    """
    Returns a dictionary that maps signal patterns to digits.
    Needs sorting so we can match with output.
    """
    decoder = {}
    for k, v in potential.items():
        if v:
            v_lst = list(v)
            v_lst.sort()
            decoder[''.join(v_lst)] = k
    return decoder

def part_2(_input):
    part_2_score = 0

    for line in _input:
        full_line = line.replace(' | ', ' ')
        potential = {}

        # First, start with the signals we can immediately attribute to a number (unique length)
        for signal in full_line.split(' '):
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
        for signal in full_line.split(' '):
            signal = set(signal)
            if len(signal) == 5:
                if potential[4] and len(potential[4].difference(signal)) == 2:
                    potential[2] = signal
                elif potential[1] and len(potential[1].difference(signal)) == 1:
                    potential[5] = signal
                elif potential[1] and len(potential[1].difference(signal)) == 0:
                    potential[3] = signal
                else:
                    raise Exception("Missing logic to detect len 5 signal code.")
            elif len(signal) == 6:
                if potential[1] and len(potential[1].difference(signal)) == 1:
                    potential[6] = signal
                elif potential[4] and len(potential[4].difference(signal)) == 1:
                    potential[0] = signal
                elif potential[4] and len(potential[4].difference(signal)) == 0:
                    potential[9] = signal
                else:
                    raise Exception("Missing logic to detect len 6 signal code.")

        # Decode the characters in the output, add to score
        decoder = get_decoder(potential)
        output_str = line.split(' | ')[1]
        output_list = [''.join(sorted(s)) for s in output_str.split(' ')]
        output_code = [str(decoder[segment]) for segment in output_list]
        part_2_score += int(''.join(output_code))

    return part_2_score


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
