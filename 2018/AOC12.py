def process_input(_input):
    change_dict = {}
    initial_state = _input[0].replace('initial state: ', '')

    for line in _input[2:]:
        _state, _growth = line.split(' => ')
        if _growth == '#':
            change_dict[_state] = _growth

    return initial_state, change_dict


def find_position(_input, i):
    _center = _input[i]

    if i >= 2:  # could be reworked into a while loop
        _left = _input[i - 2:i]
    elif i == 1:
        _left = '.' + _input[0]
    else:
        _left = '..'

    if i <= len(_input) - 3:  # same
        _right = _input[i + 1:i + 3]
    elif i == len(_input) - 2:
        _right = _input[len(_input) - 1] + '.'
    else:
        _right = '..'

    return _left + _center + _right


def main(_input, max_t):
    sol = []
    padding = '.........'
    pad_size = 0
    initial_state, change_dict = process_input(_input)

    for t in range(max_t):
        if '#' in initial_state[:5]:
            initial_state = padding + initial_state
            pad_size += len(padding)
        if '#' in initial_state[len(initial_state) - 5:]:
            initial_state = initial_state + padding

        new_sol = sum([ix - pad_size for ix, v in enumerate(initial_state) if v == '#'])
        sol.append(new_sol)

        new_state = ''

        for i in range(len(initial_state)):
            position = find_position(initial_state, i)

            if position in change_dict.keys():
                new_state += change_dict[position]
            else:
                new_state += '.'

        initial_state = new_state
        print(initial_state)

    return sol


if __name__ == "__main__":
    _input = open('2018/aoc_12.txt').read().splitlines()

    sol1 = main(_input, 1001)
    print(f'PART 1: {sol1[20]}')  # 2444

    print('\n PART 2')
    #  for s in range(950, 1001): print(s, sol1[s])  # noticing a pattern: growing by 15
    print((50000000000 - 1000) * (sol1[1000] - sol1[999]) + sol1[1000])  # 750000000697
