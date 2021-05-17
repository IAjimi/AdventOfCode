'''Initial solution iterated through the nodes like a graph traversal problem. To work properly
for larger examples, would have needed to keep track of remaining quantity of material over time.

This solution borrows from https://github.com/jcisio/adventofcode2019/blob/master/day14/d14.py
Every ingredient is visited by order of increasing distance from FUEL. All ingredients used to
create this material are added to the running total.
'''

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

def traverse_nodes(_input, distance={}, material='FUEL', n = 0):
    if material not in distance.keys():
        distance[material] = n
    else:
        distance[material] = max(n, distance[material])

    if material in _input.keys():
        inc, next_nodes = _input[material]

        for new_m, new_q in next_nodes:
            distance = traverse_nodes(_input, distance, new_m, n + 1)

    return distance

def compute_ore_requirement(transform_mapping,n_fuel=1):
    needed = {'FUEL': n_fuel}
    while len(needed) > 1 or 'ORE' not in needed.keys():
        material = min(needed, key=lambda x: distance[x])
        quantity = needed[material]
        del needed[material]
        inc, ingredients = transform_mapping[material]
        for new_m, new_q in ingredients:
            if new_m not in needed:
                needed[new_m] = 0
            needed[new_m] += math.ceil(quantity / inc) * new_q

    return needed['ORE']


def guess_sol2(first_guess):
    min_guess, max_guess = int(1000000000000 / first_guess), 2 * int(1000000000000 / first_guess)
    guess = min_guess
    found = False

    while not found:
        sol2 = compute_ore_requirement(transform_mapping, guess)

        if (sol2 == 1000000000000) or (max_guess - min_guess == 1):
            return guess
        elif sol2 > 1000000000000:  # guess is too high
            max_guess = guess
        elif sol2 < 1000000000000:  # guess is too low
            min_guess = guess

        guess = int((min_guess + max_guess) / 2)

if __name__ == '__main__':
    _input = open("2019/aoc14.txt").read().splitlines()
    transform_mapping = get_transform_mapping(_input)
    distance = traverse_nodes(transform_mapping, distance={}, material='FUEL')

    sol1 = compute_ore_requirement(transform_mapping)  # 1590844
    print(f'PART 1: {sol1}')

    sol2 = guess_sol2(sol1)
    print(f'PART 2: {sol2}')  # 1184209


