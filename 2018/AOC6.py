def manhattan_distance(t1, t2):
    '''

    :param t1: tuple
    :param t2: tuple
    :return: int
    '''
    x1, y1 = t1
    x2, y2 = t2

    return abs(x1 - x2) + abs(y1 - y2)

def find_bounded_points(_input):
    '''
    Alternate would be to find points that have the shortest distance to locations near
    the boundary with something like (see below) in compute_distance
    # if x <= min_x + 10 and y <= min_y + 10: bound_2.append(min_d)

    :param _input:
    :return:
    '''
    bounded = []

    for ix, i in enumerate(_input):
        x, y = i
        t = [0, 0, 0, 0]
        for j in _input:
            if i != j:
                if (j[0] <= x and j[1] < y):  # top left quadrant
                    t[0] = 1
                elif (j[0] >= x and j[1] < y):  # top right quadrant
                    t[1] = 1
                elif (j[0] >= x and j[1] > y):  # bottom right quadrant
                    t[2] = 1
                elif (j[0] <= x and j[1] > y):  # bottom left quadrant
                    t[3] = 1
        if sum(t) == 4:
            bounded.append(ix)

    return bounded

def compute_distance(_input):
    region = 0
    dist = [0 for i in _input]

    min_x = min([t[0] for t in _input])
    max_x = max([t[0] for t in _input])
    min_y = min([t[1] for t in _input])
    max_y = max([t[1] for t in _input])

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            t = (x, y)
            d = [manhattan_distance(t, i) for i in _input]

            # Find closest point
            _min = min(d)
            if d.count(_min) == 1:
                min_d = d.index(_min)
                dist[min_d] += 1

            # Check if in region
            if sum(d) < 10000:
                region += 1

    return dist, region

if __name__ == '__main__':
    _input = open("2018/aoc_6.txt").read().splitlines()
    _input = [tuple(map(int, i.split(','))) for i in _input]
    bounded = find_bounded_points(_input)
    dist, region = compute_distance(_input)
    bounded_dist = [dist[b] for b in bounded]
    bounded_dist.sort()
    print(f'PART 1: {bounded_dist[-3:]}')  # 3260
    print(f'PART 2: {region}')  # 42535