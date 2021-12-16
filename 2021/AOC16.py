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


def parse_hex(decoded_str: str, version_sum: int = 0):
    if decoded_str:
        total = 0
        packet_version = int(decoded_str[:3], 2)
        packet_type_id = int(decoded_str[3:6], 2)
        decoded_str = decoded_str[6:]
        version_sum += packet_version

        # print(packet_version, packet_type_id, decoded_str[0], decoded_str)

        if packet_type_id == 4:
            total, decoded_str = get_literal_value(decoded_str)
        else:
            length_type_id = decoded_str[0]
            if length_type_id == "0":
                subpacket_len = int(decoded_str[1:16], 2)
                subpacket = decoded_str[16 : 16 + subpacket_len]
                while subpacket:
                    packet_version, value, subpacket = parse_hex(subpacket)
                    total += value
                    version_sum += packet_version
                decoded_str = decoded_str[16 + subpacket_len :]
            elif length_type_id == "1":
                subpacket_num = int(decoded_str[1:12], 2)
                decoded_str = decoded_str[12:]
                for r in range(subpacket_num):
                    packet_version, value, decoded_str = parse_hex(decoded_str)
                    total += value
                    version_sum += packet_version

        return version_sum, total, decoded_str
    else:
        return version_sum, 0, ""


def decode_string(str_to_hex_decoder: dict, string: str):
    decoded_str = "".join([str_to_hex_decoder[char] for char in string])
    version_sum = parse_hex(decoded_str)
    return version_sum


def part_1(string):
    str_to_hex_decoder = create_decoder(hexa_decoder_str)
    part_1_score, _, _ = decode_string(str_to_hex_decoder, string)
    return part_1_score


@timer
def main(filepath: str):
    _input = read_input(filepath)
    string = _input[0]
    str_to_hex_decoder = create_decoder(hexa_decoder_str)
    part_1_score, _, _ = decode_string(str_to_hex_decoder, string=string)  # 866
    part_2_score = 0
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc16.txt")
    print(f"PART 1: {part_1_score}")  # .
    print(f"PART 2: {part_2_score}")  # .
