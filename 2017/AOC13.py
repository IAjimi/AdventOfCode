def process_input(_input):
    _input = [i.split(': ') for i in _input]

    depths = {int(k): int(v) for k, v in _input}
    _max = max(depths.keys())
    _len = len(depths.keys())
    return depths, _max, _len


def calculate_severity(depths, _max):
    severity = 0

    for n in range(1, _max + 1):
        if n in depths.keys():
            r = depths[n]
            if n % (2 * (r - 1)) == 0:
                severity += n * r

    return severity

def calculate_intercepts(depths, _max, _len):
    i = 0
    _sum = 0
    _find = False

    while not _find and i < 10000000:
        for n in depths.keys():
            r = depths[n]
            _bool = (i + n) % (2 * (r - 1))
            _sum += 1 if _bool != 0 else 0

        if _sum == _len:
            return i
        else:
            _sum = 0
            i += 1

if __name__ == "__main__":
    _input = open("2017/aoc_13.txt").read().splitlines()
    depths, _max, _len = process_input(_input)

    sol1 = calculate_severity(depths, _max)  # 3184
    sol2 = calculate_intercepts(depths, _max, _len)
    print(f"PART 1: {sol1} \n PART 2: {sol2}")

    # _max = 6
    # for _ in range(20):
    #     n = _ % _max
    #     if n in depths.keys():
    #         r = depths[n]
    #         _sum = _ % (2 * (r - 1))
    #         _sum = 1 if _sum != 0 else 0
    #         print(_sum)


    ## SEQUENCE OF LENGTH _max
    ## convert to 1 if not 0
    ## create stopgap vectors for the things in between that are just 1
    ## sum em
    ## find earliest sum of vectors of length n that matches
