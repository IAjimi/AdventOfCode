def redistribute_memory(_input):
    n = len(_input)

    states = []
    repeated = False
    t = 0

    while not repeated:
        s = ''.join([str(i) for i in _input])
        if s in states:
            states.append(s)
            return t, states
        else:
            states.append(s)

        max_val = max(_input)
        max_ix = _input.index(max_val)
        _input[max_ix] = 0 # reset this
        ix = max_ix

        while max_val > 0:
            ix = (ix + 1) % n
            _input[ix] += 1
            max_val += -1

        t += 1

if __name__ == "__main__":
    _input = open("2017/aoc_6.txt").read().split()
    _input = [int(i) for i in _input]

    sol1, states = redistribute_memory(_input.copy()) # 14029
    sol2 = sol1 - states.index(states[-1]) # 2765
    print(f"PART 1: {sol1} \n PART 2: {sol2}")