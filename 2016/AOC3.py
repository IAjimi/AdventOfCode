def check_triangle(line):
    _max = max(line)
    ix_max = line.index(_max)
    sides = line[:ix_max] + line[ix_max+1:]

    if sum(sides) > _max:
        return 1
    else:
        return 0

if __name__ == '__main__':
    _input = open("2016/aoc3.txt").read().splitlines()

    _input = [list(map(int, " ".join(i.split()).split(' '))) for i in _input]  # ugly way to deal w/ uneven spacing
    sol1 = sum([check_triangle(line) for line in _input])
    print(f'PART 1: {sol1}')  # 1050

    reworked_list = [[_input[r][i], _input[r + 1][i], _input[r + 2][i]] for r in range(0, len(_input), 3) for i in range(3)]
    sol2 = sum([check_triangle(line) for line in reworked_list])
    print(f'PART 2: {sol2}')  # 1921
