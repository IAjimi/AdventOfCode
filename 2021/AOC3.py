from _utils import read_input

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
    gamma_rate = "".join([most_common_bit(_input, i) for i in range(len(_input[0]))])
    epsilon_rate = "".join(
        ["0" if bit == "1" else "1" for bit in gamma_rate]
    )  # flip gamma_rate
    return compute_answer(gamma_rate, epsilon_rate)

def part_2(_input: list):
    oxy_gen_rating = find_rating(_input, most_common=True)
    co2_rating = find_rating(_input, most_common=False)
    return compute_answer(oxy_gen_rating, co2_rating)


if __name__ == "__main__":
    _input = read_input("2021/aoc3.txt")

    print(f"PART 1: {part_1(_input)}")  # 3958484
    print(f"PART 2: {part_2(_input)}")  # 1613181
