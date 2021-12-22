"""
One of the more challenging days for me. Forgot to operate on a
subpacket, not the whole string, for one of the sub-operations
(decoded_str = decoded_str[15 + subpacket_len :]).
"""
from typing import Tuple, Dict

from _utils import read_input, timer, product


def create_decoder() -> Dict[str, str]:
    hex_decoder_str = read_input("hex_decoder_aoc16.txt")
    str_to_hex_decoder = {}

    for line in hex_decoder_str:
        key, val = line.split(" = ")
        str_to_hex_decoder[key] = val

    return str_to_hex_decoder


def get_literal_value(decoded_str: str) -> Tuple[int, str]:
    packed_bits = []

    for r in range(0, len(decoded_str), 5):
        str_segment = decoded_str[r : r + 5]

        if len(str_segment) == 5:
            leading_bit = str_segment[0]
            actual_bit = str_segment[1:]
            packed_bits.append(actual_bit)

            if leading_bit == "0":
                packed_bits = "".join(packed_bits)
                return int(packed_bits, 2), decoded_str[r + 5 :]

    packed_bits = "".join(packed_bits)
    return int(packed_bits, 2), ""


def compute_value(operation_id: int, values: list) -> int:
    """
    Returns the result of an operation on the values list.
    """
    operations_list = [
        sum,
        product,
        min,
        max,
        sum,
        lambda x: int(x[0] > x[1]),
        lambda x: int(x[0] < x[1]),
        lambda x: int(x[0] == x[1]),
    ]
    try:
        return operations_list[operation_id](values)
    except IndexError:
        raise Exception(f"Operation {operation_id} is not implemented by calculator.")
    except Exception as e:
        raise e


def parse_hex(decoded_str: str, version_sum: int = 0) -> Tuple[int, str, int, int]:
    """
    Parse a binary representation of a packet.

    Returns the sum of packet versions contained in packet,
    the value of the packet, the remaining un-parsed parts of
    the binary rep (if applicable), and the packet_type_id.
    """
    packet_version = int(decoded_str[:3], 2)
    packet_type_id = int(decoded_str[3:6], 2)
    decoded_str = decoded_str[6:]
    version_sum += packet_version
    values = []

    if packet_type_id == 4:
        val, decoded_str = get_literal_value(decoded_str)
        values.append(val)
    else:
        length_type_id = decoded_str[0]
        decoded_str = decoded_str[1:]
        if length_type_id == "0":
            subpacket_len = int(decoded_str[:15], 2)
            subpacket = decoded_str[15 : 15 + subpacket_len]
            while subpacket:
                packet_version, val, subpacket, _ = parse_hex(subpacket)
                version_sum += packet_version
                values.append(val)
            decoded_str = decoded_str[15 + subpacket_len :]
        elif length_type_id == "1":
            subpacket_num = int(decoded_str[:11], 2)
            decoded_str = decoded_str[11:]
            for r in range(subpacket_num):
                packet_version, val, decoded_str, _ = parse_hex(decoded_str)
                values.append(val)
                version_sum += packet_version

    val = compute_value(packet_type_id, values)
    return version_sum, val, decoded_str, packet_type_id


def get_solution(string: str) -> Tuple[int, int]:
    """
    Returns part 1 & 2 scores from an operator packet string.

    Ex:
        get_solution(string="9C0141080250320F1802104A08")
        > (20, 1)
    """
    str_to_hex_decoder = create_decoder()
    decoded_str = "".join([str_to_hex_decoder[char] for char in string])
    sum_packet_version, value, *_ = parse_hex(decoded_str)
    return sum_packet_version, value


@timer
def main(filepath: str) -> Tuple[int, int]:
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    string = _input[0]
    part_1_score, part_2_score = get_solution(string)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc16.txt")
    print(f"PART 1: {part_1_score}")  # 866
    print(f"PART 2: {part_2_score}")  # 1392637195518
