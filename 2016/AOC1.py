def walk(_input, part):
    x, y = 0, 0
    direction = 0
    dir_mapping = {0: (0, -1), 90: (1, 0), 180: (0, 1), 270: (-1, 0)}
    visited = []

    for line in _input:
        _dir = line[0]
        val = int(line[1:])

        if _dir == 'R':
            direction += 90
        elif _dir == 'L':
            direction += -90
        else:
            raise Exception('Only L and R are valid directions!')

        direction = direction % 360
        move = dir_mapping[direction]

        if part == 1:
            x += val * move[0]
            y += val * move[1]
        elif part == 2:
            for i in range(val):
                x += move[0]
                y += move[1]

                if (x, y) in visited:
                    return abs(x) + abs(y)

                visited.append((x,y))

    return abs(x) + abs(y)

if __name__ == '__main__':
    _input = open("2016/aoc1.txt").read().split(', ')
    sol1 = walk(_input, part=1)  # 332
    sol2 = walk(_input, part=2)  # 166
    print(f'PART 1: {sol1} \n PART 2: {sol2}')
