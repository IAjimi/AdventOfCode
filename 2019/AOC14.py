# 157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT

# FUEL, 44 XJWVT
# 2 XJWVT = 7 DCFZ, 7 PSHF -> (2, [('DCFZ', 7), ('PSHF', 7)]) -> 44 / 2 = 22
# 22 * 7 DCFZ = 154
# 6 DCFZ = 165 ORE -> ceil(154 / 6) = 26
# 26 * 154 ORE = 4004







import math

def get_num_and_letter(string):
    num, letter = string.split(' ')
    return letter, int(num)

def get_transform_mapping(_input):
    transform_mapping = {}

    for line in _input:
        _from, _to = line.split(' => ')
        letter_to, q_to = get_num_and_letter(_to)
        _from = [get_num_and_letter(val) for val in _from.split(', ')]
        _from = [(num, val / q_to) for num, val in _from]
        transform_mapping[letter_to] = _from

    return transform_mapping

def get_ore_repo(_input):
    ore_repo = {}

    for line in _input:
        if 'ORE' in line:
            _from, _to = line.split(' => ')
            letter_from, q_from = get_num_and_letter(_from)
            letter_to, q_to = get_num_and_letter(_to)

            ore_repo[letter_to] = (q_from, q_to)

    return ore_repo


def traverse_nodes(_input, used={}, material='FUEL', quantity=1):
    next_nodes = _input[material]
    print(material, next_nodes, used)

    for nn in next_nodes:
        new_m, new_q = nn
        #import pdb; pdb.set_trace()

        if new_m == 'ORE':
            if material in used.keys():
                used[material] += quantity
            else:
                used[material] = quantity

            return used
        else:
            used = traverse_nodes(_input, used, new_m, new_q * quantity)
            print(material, quantity, used)

    print('\n')
    return used

if __name__ == '__main__':
    _input = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''.splitlines()

    _input = '''9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL'''.splitlines()

    _input = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''.splitlines()

    transform_mapping = get_transform_mapping(_input)
    ore_repo = get_ore_repo(_input)

    used = traverse_nodes(transform_mapping, used={}, material='FUEL', quantity=1)

    total_ore = 0

    for m,q in used.items():
        ore, not_ore = ore_repo[m]
        total_ore += math.ceil(math.ceil(q) / not_ore) * ore
        print(m,q, math.ceil(math.ceil(q) / not_ore) * ore)

    print(total_ore)
