def read_input(filepath):
    with open(filepath) as _input:
        return [int(i) for i in _input.read().splitlines()]


def count_increase(_input):
    counter = 0

    for i in range(1, len(_input)):
        curr = _input[i]
        prev = _input[i - 1]

        if curr > prev:
            counter += 1

    return counter


def count_sliding_window_increase(_input):
    counter = 0

    for i in range(1, len(_input) - 2):
        curr = _input[i + 2]
        prev = _input[i - 1]

        if curr > prev:
            counter += 1

    return counter


if __name__ == "__main__":
    _input = read_input("2021/aoc1.txt")

    counter = count_increase(_input)
    print(f"PART 1: {counter}")  # 1233

    counter = count_sliding_window_increase(_input)
    print(f"PART 2: {counter}")  # 1275
