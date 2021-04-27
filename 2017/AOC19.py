# go thru priority up down left right
# != prev

def parse_input(_input):
    grid = {}

    for i in range(len(_input)):
        line = _input[i]
        for j in range(len(line)):
            s = line[j]
            if s.isalpha() or (not s.isalpha()) and (s != ' '):
                grid[(i, j)] = s

    return grid

def find_neighbors(grid, i,j):
    neighbors_list = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    neighbors_list = [neigh for neigh in neighbors_list if neigh in grid.keys()]
    return neighbors_list

def walk_path(grid, start):
    path = []
    letters = []
    i, j = start
    neigh = i,j
    prev = 0,0

    while len(letters) < 10:
        ## CONTINUE GOING THE SAME DIRECTION
        direction = (neigh[0] - prev[0], neigh[1] - prev[1])
        if direction in [(0, 1), (0, -1)]:
            neighbors_list = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
        else:
            neighbors_list = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]

        for neigh in neighbors_list:
            if neigh in grid.keys() and neigh != prev:
                prev = i, j
                i, j = neigh  # moving forward

                path.append(grid[(i, j)])
                break

        letters = [p for p in path if p.isalpha()]

    return ''.join(letters), path

if __name__ == "__main__":
    _input = open("2017/aoc_19.txt").read().splitlines()

    grid = parse_input(_input)
    start = [g for g in grid.keys() if g[0] == 0][0]

    sol1, path = walk_path(grid, start) # ITSZCJNMUO
    sol2 = len(path) + 1 # 17420

    print(f"PART 1: {sol1} \n PART 2: {sol2}")