def parse_grid(_input):
    grid = {(x, y): _input[y][x] for y in range(len(_input)) for x in range(len(_input[y])) if _input[y][x] != '#'}
    keys = {v:k for k,v in grid.items() if v in 'abcdefghijklmnop'}
    doors = {v:k for k,v in grid.items() if v in 'ABCDEFGHIJKLMNOP'}
    start = [k for k,v in grid.items() if '@' in v]
    return grid, keys, doors, start

def trace_steps(grid, pos):
    start = pos
    visited = [pos]
    paths = {}
    move = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while set(visited) != set(grid.keys()):
        print('back to start')
        pos = start
        reset = False
        steps = 0
        doors = []

        while not reset:
            changed = False

            for dx, dy in move:
                new_pos = pos[0] + dx, pos[1] + dy

                if new_pos in grid.keys() and new_pos not in visited:
                    print(new_pos, grid[new_pos], steps, doors)
                    val = grid[new_pos]
                    steps += 1

                    if val in 'abcdefgh':
                        paths[val] = {'steps': steps, 'doors': set(doors)}
                    elif val in 'ABCDEFGH':
                        doors.append(val.lower())

                    visited.append(new_pos)
                    pos = new_pos
                    changed = True
            if not changed:
                reset = True

    return paths

def find_nodes(keypaths, current_node='@0', path=[], steps=0):
    while len(path) != len(keypaths.keys()):
        path.append(current_node)
        possible_paths = [k for k, v in keypaths[current_node].items() if k != current_node and k not in path and v['doors'].difference(set(path)) == set()]
        print(current_node, path, possible_paths, steps)

        if not possible_paths:
            return steps, path
        elif len(possible_paths) == 1:
            node = possible_paths[0]
        else: # use recursion to determine best of multiple steps
            all_steps = {poss_node: find_nodes(keypaths, poss_node, path.copy(), steps)[0] for poss_node in possible_paths}
            node = [k for k, v in all_steps.items() if v == min(all_steps.values())][0]


        steps += keypaths[current_node][node]['steps']
        current_node = node

    return steps, path

if __name__ == '__main__':
    _input = '''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''.splitlines()
    _input = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''.splitlines()

    grid, keys, doors, start = parse_grid(_input)
    keypaths = {key: trace_steps(grid, key_pos) for key, key_pos in keys.items()}
    keypaths['@0'] = trace_steps(grid, start[0])
    steps, path = find_nodes(keypaths, current_node='@0', path=[], steps=0)

