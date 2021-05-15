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
        transform_mapping[letter_to] = (q_to, _from)

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
    inc, next_nodes = _input[material]
    print(material, quantity, _input[material], used)

    for nn in next_nodes:
        new_m, new_q = nn

        if new_m == 'ORE':
            if material in used.keys():
                used[material] += quantity
            else:
                used[material] = quantity

            return used
        else:
            used = traverse_nodes(_input, used, new_m, new_q * math.ceil(quantity / inc))
            print(material, quantity, used)

    print('\n')
    return used

if __name__ == '__main__':
    _input = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF'''.splitlines()

    transform_mapping = get_transform_mapping(_input)
    ore_repo = get_ore_repo(_input)

    used = traverse_nodes(transform_mapping, used={}, material='FUEL', quantity=1)

    total_ore = 0

    for m,q in used.items():
        ore, not_ore = ore_repo[m]
        total_ore += math.ceil(math.ceil(q) / not_ore) * ore
        print(m,q, math.ceil(math.ceil(q) / not_ore) * ore)

    print(total_ore)

# {'MNCFX': 4192, 'VJHF': 1989, 'NVRVD': 551, 'JNWZP': 78} ## CORRECT
# {'NVRVD': 571, 'JNWZP': 81, 'VJHF': 2011, 'MNCFX': 4229} ## CURRENT