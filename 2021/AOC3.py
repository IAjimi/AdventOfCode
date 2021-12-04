from _utils import read_input, timer


def most_common_bit(bin_list: list, ix: int):
    """
    Returns the most common bit as str in position i of the list
    of binary numbers _input.
    """
    n = len(bin_list)
    most_common = sum([int(row[ix]) for row in bin_list])

    if most_common >= n / 2:  # 1 is tie-breaker
        return "1"
    else:
        return "0"


def find_rating(_input: list, most_common: bool):
    """
    Returns the binary number that represents the submarine's rating.

    This is done by finding the most common value (0 or 1) in the current bit position and
    iteratively filtering the list to keep only numbers with that bit in that position until
    only one number is left.
    """
    rating = _input[:]  # create copy of input to avoid changing the original
    max_ix = len(_input[0])
    ix = 0

    while ix < max_ix:
        bit = most_common_bit(rating, ix)

        if most_common:
            rating = [bin_str for bin_str in rating if bin_str[ix] == bit]
        else:
            rating = [bin_str for bin_str in rating if bin_str[ix] != bit]

        if len(rating) == 1:
            return rating[0]

        ix += 1

    raise Exception("Issue found with filtering in found_rating.")


def compute_answer(bin_1: str, bin_2: str):
    """
    Returns the product of two binary numbers.
    """
    bin_to_int_1 = int(bin_1, 2)
    bin_to_int_2 = int(bin_2, 2)
    return bin_to_int_1 * bin_to_int_2


def part_1(_input: list):
    """
    Returns the product of the gamma and epsilon rates.

    The gamma rate is the binary number created by joining
    together the most common bits across the list for every
    position in the binary number. The epsilon rate is the opposite
    of the gamma rate.
    """
    gamma_rate = "".join([most_common_bit(_input, i) for i in range(len(_input[0]))])
    epsilon_rate = "".join(
        ["0" if bit == "1" else "1" for bit in gamma_rate]
    )  # flip gamma_rate
    return compute_answer(gamma_rate, epsilon_rate)


def part_2(_input: list):
    """
    Returns the product of the oxygen generator rating
    and CO2 scrubber rating.
    """
    oxy_gen_rating = find_rating(_input, most_common=True)
    co2_rating = find_rating(_input, most_common=False)
    return compute_answer(oxy_gen_rating, co2_rating)


@timer
def main(filename: str):
    _input = read_input(filename)
    part_1_score = part_1(_input)
    part_2_score = part_2(_input)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc3.txt")
    print(f"PART 1: {part_1_score}")  # 3958484
    print(f"PART 2: {part_2_score}")  # 1613181
