def parse_input(line):
    '''Takes a string of a specific format and returns
    a list of list(int).

    > line = p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
    > parse_input(line)
    # [[3, 0, 0], [2, 0, 0], [-1, 0, 0]]

    :param line: str, see format above
    :return: list[list[int]]
    '''
    line = line.split(', ')
    line = [s[3:-1].split(',') for s in line]
    line = [list(map(int, l)) for l in line]
    return line

def get_input():
    _input = open("2017/aoc_20.txt").read().splitlines()
    _input = [parse_input(line) for line in _input]
    return _input

def manhattan_distance(coord):
    ''' Takes in list of coordinates (x, y, z), returns
    Manhattan Distance (sum of absolute value of the coordinates.

    > [3, -2, 5]
    > 10

    :param coord: list[int]
    :return: int
    '''
    coord = [abs(c) for c in coord]
    return sum(coord)

def run_particles(_input, find_collisions):
    max_t = 350 # semi-arbitrary choice - after this point, sol1 doesn't change

    for t in range(1, max_t + 1):
        for line in _input:
            # line[0] is p=<>, line[1] is v=<>, line[2] is a=<>
            line[0][0] += line[1][0] + line[2][0] * t
            line[0][1] += line[1][1] + line[2][1] * t
            line[0][2] += line[1][2] + line[2][2] * t

        positions = {}
        for line in _input:
            l = tuple(line[0])
            if l in positions.keys():
                positions[l] += 1
            else:
                positions[l] = 1

        if find_collisions:
            collisions = [pos for pos,count in positions.items() if count > 1]
            _input = [line for line in _input if tuple(line[0]) not in collisions]

    return _input

if __name__ == '__main__':
    _input = get_input()
    _input = run_particles(get_input(), find_collisions=False)
    dist = [manhattan_distance(line[0]) for line in _input]
    sol1 = dist.index(min(dist))  # 157

    _input = get_input()
    _input = run_particles(_input, find_collisions=True)
    sol2 = len(_input)  # 499
    
    print(f'PART 1: {sol1} \n PART 2: {sol2}')