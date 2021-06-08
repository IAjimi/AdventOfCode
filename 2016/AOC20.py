'''Fun puzzle. Couple of things to make this run quick.

1) the ranges in the _input are ordered by the minimum bound
instead of [(5, 8), (0, 2), (4, 7)], have [(0, 2), (4, 7), (5, 8)]
2) this means that when testing for unblocked ips, you can directly skip
to the max bound of the range without being worried

-> start at 0, 0 is in (0, 2) so skip to 3
-> 3 iterates over remaining bounds ((4, 7) and (5, 8)) and is in neither
= part 1 solution
-> for part 2, go to 4, 4 is in within (4, 7) bounds so jump to 8
-> 8 is in (5, 8) bounds so jump to 9
-> there are no remaining bounds and 9 <= 9
= part 2 solution
'''

def clean_input(_input):
    _input = [tuple(map(int, i.split('-'))) for i in _input]
    _input.sort(key=lambda x: x[0])
    return _input

def find_unblocked_ip(_input, max_n, part):
    r, n = 0, 0

    while r <= max_n:
        for tup in _input:
            _min, _max = tup
            if r >= _min and r <= _max:
                r = _max + 1

        if part == 1:
            return r  # return the first match
        else:
            r += 1
            if r <= max_n:  # only count numbers that are withing bound
                n += 1

    return n  # return the number of matches


if __name__ == '__main__':
    _input = open("2016/aoc20.txt").read().splitlines()
    _input = clean_input(_input)

    sol1 = find_unblocked_ip(_input, max_n=4294967295, part=1)  # 17348574
    sol2 = find_unblocked_ip(_input, max_n=4294967295, part=2)  # 104
    print(f'PART 1: {sol1} \n PART 2: {sol2}')