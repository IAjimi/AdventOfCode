''' Learning from https://www.reddit.com/r/adventofcode/comments/7lte5z/2017_day_24_solutions/

build_strong_bridges function comes from ythl'''


def build_strong_bridges(c, match_val):
    _sum = 0
    path = []

    for i, comp in enumerate(c):
        if match_val in comp:
            mv = comp[0] if comp[0] != match_val else comp[1]
            p = comp + build_strong_bridges(c[:i] + c[i + 1:], mv)

            if sum(p) > _sum:
                _sum = sum(p)
                path = p

    return path


def build_long_bridges(c, match_val):
    _len = 0
    _sum = 0
    path = []

    for i, comp in enumerate(c):
        if match_val in comp:
            mv = comp[0] if comp[0] != match_val else comp[1]
            p = comp + build_long_bridges(c[:i] + c[i + 1:], mv)

            if (len(p) >= _len) and (sum(p) >= _sum):
                _len = len(p)
                _sum = sum(p)
                path = p

    return path

if __name__ == '__main__':
    _input = open("2017/aoc_24.txt").read().splitlines()
    c = [list(map(int, line.split("/"))) for line in _input]

    sol1 = sum(build_strong_bridges(c, 0))   # 1656
    print(f'PART 1: {sol1}')
    sol2 = sum(build_long_bridges(c, 0))  # 1642
    print(f'PART 2: {sol2}')
