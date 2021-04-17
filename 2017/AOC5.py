def process_instructions_pt1(_input):
    n = 0
    ix = 0

    while ix < len(_input):
        offset = _input[ix]
        _input[ix] += 1
        ix += offset
        n += 1

    return n

def process_instructions_pt2(_input):
    n = 0
    ix = 0

    while ix < len(_input):
        offset = _input[ix]
        _input[ix] += -1 if offset >= 3 else 1
        ix += offset
        n += 1

    return n


if __name__ == "__main__":
    _input = open("2017/aoc_5.txt").read().splitlines()
    _input = [int(i) for i in _input]

    sol1 = process_instructions_pt1(_input.copy()) # 360603
    sol2 = process_instructions_pt2(_input.copy()) # 25347697
    print(f"PART 1: {sol1} \n PART 2: {sol2}")