from functools import reduce

def twist_knots(_input, _input_len, _start, skip_size):
    n = len(_input)

    for i in range(len(_input_len)):
        temp = _input.copy()
        current_len = _input_len[i]
        _end = _start + current_len

        pos = [r % n for r in range(_start, _end)]
        val = [_input[p] for p in pos][::-1]
        combo = [*zip(pos, val)]

        for p, v in combo:
            temp[p] = v

        _start = (_start + current_len + skip_size) % n
        _input = temp

        skip_size += 1

    return _input, _start, skip_size

def main(_input, _input_len, _start, skip_size, rounds):
    for r in range(rounds):
        _start = _start % len(_input)
        _input, _start, skip_size = twist_knots(_input, _input_len, _start, skip_size)

    if rounds == 1:
        return _input[0] * _input[1]
    else:
        dense = [] # creds to https://www.reddit.com/r/adventofcode/comments/7irzg5/2017_day_10_solutions/
        for x in range(0, 16):
            subslice = _input[16 * x:16 * x + 16]
            dense.append('%02x' % reduce((lambda x, y: x ^ y), subslice))
        return ''.join(dense)

if __name__ == "__main__":
    _input = [r for r in range(256)]
    _input_len = open("2017/aoc_10.txt").read()

    pt1_input_len = list(map(int, _input_len.split(',')))
    pt2_input_len = list(map(ord, _input_len))
    pt2_input_len.extend([17, 31, 73, 47, 23])

    sol1 = main(_input, pt1_input_len, 0, 0, 1) # 2928
    sol2 = main(_input, pt2_input_len, 0, 0, 64) # 0c2f794b2eb555f7830766bf8fb65a16
    print(f"PART 1: {sol1} \n PART 2: {sol2}")

