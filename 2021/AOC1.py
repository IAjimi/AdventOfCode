def read_input(filepath):
    _input = open(filepath).read().splitlines()
    _input = [int(i) for i in _input]
    return _input


def count_increase(_input):
    counter = 0

    for i in range(1, len(_input)):
        curr, prev = _input[i], _input[i - 1]
        if curr > prev:
            counter += 1

    return counter


def count_sliding_window_increase(_input):
    counter = 0
    prev = _input[0] + _input[1] + _input[2]

    for i in range(1, len(_input) - 2):
        curr = prev - _input[i - 1] + _input[i + 2]

        if curr > prev:
            counter += 1

        prev = curr

    return counter


if __name__ == "__main__":
    _input = read_input("2021/aoc1.txt")

    counter = count_increase(_input)
    print(f"PART 1: {counter}")  # 1233

    counter = count_sliding_window_increase(_input)
    print(f"PART 2: {counter}")  # 1275
