from _utils import read_input, timer

hexa_decoder_str = """0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111"""


def create_decoder(hexa_decoder_str: str):
    hexa_decoder_str = hexa_decoder_str.splitlines()
    str_to_hex_decoder = {}

    for line in hexa_decoder_str:
        key, val = line.split(" = ")
        str_to_hex_decoder[key] = val

    return str_to_hex_decoder


def get_literal_value(decoded_str: str):
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


def product(lst: list):
    result = 1
    for num in lst:
        result *= num
    return result


def compute_value(operation_id: int, values: list):
    if operation_id == 0:
        return sum(values)
    elif operation_id == 1:
        return product(values)
    elif operation_id == 2:
        return min(values)
    elif operation_id == 3:
        return max(values)
    elif operation_id == 4:
        return values[0]
    elif operation_id == 5:
        return 1 if values[0] > values[1] else 0
    elif operation_id == 6:
        return 1 if values[0] < values[1] else 0
    elif operation_id == 7:
        return 1 if values[0] == values[1] else 0
    else:
        raise Exception(f"Unknown operation id: {operation_id}")


def parse_hex(decoded_str: str, version_sum: int = 0):
    packet_version = int(decoded_str[:3], 2)
    packet_type_id = int(decoded_str[3:6], 2)
    decoded_str = decoded_str[6:]
    version_sum += packet_version
    value = []

    if packet_type_id == 4:
        val, decoded_str = get_literal_value(decoded_str)
        value.append(val)
    else:
        length_type_id = decoded_str[0]
        if length_type_id == "0":
            subpacket_len = int(decoded_str[1:16], 2)
            subpacket = decoded_str[16 : 16 + subpacket_len]
            while subpacket:
                packet_version, val, subpacket, _ = parse_hex(subpacket)
                version_sum += packet_version
                value.append(val)
            decoded_str = decoded_str[16 + subpacket_len :]
        elif length_type_id == "1":
            subpacket_num = int(decoded_str[1:12], 2)
            decoded_str = decoded_str[12:]
            for r in range(subpacket_num):
                packet_version, val, decoded_str, _ = parse_hex(decoded_str)
                value.append(val)
                version_sum += packet_version

    value = compute_value(packet_type_id, value)
    return version_sum, value, decoded_str, packet_type_id



def decode_string(str_to_hex_decoder: dict, string: str):
    decoded_str = "".join([str_to_hex_decoder[char] for char in string])
    version_sum, value, _, packet_type_id = parse_hex(decoded_str)
    return version_sum, value


@timer
def main(filepath: str):
    _input = read_input(filepath)
    string = _input[0]
    str_to_hex_decoder = create_decoder(hexa_decoder_str)
    part_1_score, part_2_score = decode_string(str_to_hex_decoder, string=string)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc16.txt")
    print(f"PART 1: {part_1_score}")  # 866
    print(f"PART 2: {part_2_score}")  # 1392637195518
