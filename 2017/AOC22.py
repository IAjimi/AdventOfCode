def pt1(current_node, grid, direction):
    if (current_node in grid.keys()) and (grid[current_node] == '#'):
        grid[current_node] = '.'
        direction += 90
        infected = 0
    else:
        grid[current_node] = '#'
        direction += -90
        infected = 1

    return grid, direction, infected

def pt2(current_node, grid, direction):
    infected = 0

    if (current_node in grid.keys()) and (grid[current_node] == '#'):
        grid[current_node] = 'F'
        direction += 90
    elif (current_node in grid.keys()) and (grid[current_node] == 'W'):
        grid[current_node] = '#'
        infected += 1
    elif (current_node in grid.keys()) and (grid[current_node] == 'F'):
        grid[current_node] = '.'
        direction += 180
    else:  # not in grid or in grid and clean
        grid[current_node] = 'W'
        direction += -90

    return grid, direction, infected

def infect_nodes(_input, part):
    grid = {(j, i): _input[i][j] for i in range(len(_input)) for j in range(len(_input[0]))}
    mid_point = max(grid.keys())[0] / 2
    current_node = (int(mid_point), int(mid_point))
    dir_mapping = {0: (0,-1), 90: (1,0), 180: (0,1), 270: (-1,0)}
    infections = 0
    direction = 0

    if part == 'PART 1':
        max_range = 10000
    else:
        max_range = 10000000

    for r in range(max_range):
        if part == 'PART 1':
            grid, direction, infected = pt1(current_node, grid, direction)
        else:
            grid, direction, infected = pt2(current_node, grid, direction)

        infections += infected

        direction = direction % 360
        move = dir_mapping[direction]
        current_node = (current_node[0] + move[0], current_node[1] + move[1])

    return infections

if __name__ == "__main__":
    _input = open("2017/aoc_22.txt").read().splitlines()

    sol1 = infect_nodes(_input, 'PART 1')  # 5450
    sol2 = infect_nodes(_input, 'PART 2')  # 2511957
    print(f'PART 1: {sol1} \n PART 2: {sol2}')

