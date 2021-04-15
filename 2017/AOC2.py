def checksum(_input):
    _sum = 0

    for x in range(len(_input)):
        line = [int(i) for i in _input[x]]
        _min, _max = min(line), max(line)
        _sum += _max - _min

    return _sum

def checkdiv(_input):
    _sum = 0

    for x in range(len(_input)):
        line = [int(i) for i in _input[x]]
        search = True

        while search:
            _min = min(line)
            line.remove(_min)
            div = [i for i in line if i % _min == 0]

            if div:
                search = False

        _sum += div[0] / _min

    return _sum

if __name__ == "__main__":
    _input = open("2017/aoc_2.txt").read().splitlines()
    _input = [i.split() for i in _input]

    sol1 = checksum(_input) # 30994
    sol2 = checkdiv(_input) # 233
    print(f"PART 1: {sol1} \n PART 2: {sol2}")