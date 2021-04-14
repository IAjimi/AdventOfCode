def get_sum(_input, n):
    _sum = 0
    size = len(_input)

    for i in range(len(_input)):
        _current = _input[i]
        _next = _input[(i + n) % size]

        if _current == _next:
            _sum += int(_input[i])

    return _sum


def main(_input, jump):
    # Clean _input
    _input = [s for s in _input]

    # Get jump size
    if jump == True:
        n = int(len(_input) / 2)
    else:
        n = 1

    _sum = get_sum(_input, n)

    return _sum


if __name__ == "__main__":
    _input = open("2017/aoc_1.txt").read()

    sol1 = main(_input, False)  # 1175
    sol2 = main(_input, True)  # 1166
    print(f"PART 1: {sol1} \n PART 2: {sol2}")