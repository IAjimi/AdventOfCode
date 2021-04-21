def get_distance(directions):
    visited = []
    north, east = 0, 0
    hex_map = {'n': (0, -1), 's': (0, 1), 'ne': (1, -1), 'se': (1, 0), 'nw': (-1, 0), 'sw': (-1, 1)}

    for d in directions:
        v = hex_map[d]
        north += v[0]
        east += v[1]
        visited.append((north, east))

    return visited

if __name__ == "__main__":
    _input = open("2017/aoc_11.txt").read().split(',')
    visited = get_distance(_input)
    sol1 = max(visited[-1]) # 818 - max gives number of steps
    sol2 = max(visited) # 1596 - chould also check min for other inputs

    print(f"PART 1: {sol1} \n PART 2: {sol2}")