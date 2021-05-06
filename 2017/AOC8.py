def parse_line(line):
    new_key, op1, new_val, _, cond_key, op2, cond_val = line.split(' ')

    op_sign = 1 if op1 == 'inc' else -1
    new_val = int(new_val)
    _bool = 'd["' + cond_key + '"]' + op2 + cond_val

    return new_key, op_sign, new_val, cond_key, _bool

def run(_input):
    d = {}
    _max = 0

    for line in _input:
        new_key, op_sign, new_val, cond_key, _bool = parse_line(line)

        if new_key not in d.keys():
            d[new_key] = 0
        if cond_key not in d.keys():
            d[cond_key] = 0

        if eval(_bool):
            d[new_key] += op_sign * new_val
            if d[new_key] > _max:
                _max = d[new_key]

    return max(d.values()), _max

if __name__ == "__main__":
    _input = open("2017/aoc_8.txt").read().splitlines()
    sol1, sol2 = run(_input)  # 8022, 9819
    print(f"PART 1: {sol1} \n PART 2: {sol2}")