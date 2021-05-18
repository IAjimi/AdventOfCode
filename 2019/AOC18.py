def parse_grid(_input):
    grid = {(x, y): _input[y][x] for y in range(len(_input)) for x in range(len(_input[y])) if _input[y][x] != '#'}
    keys = {v:k for k,v in grid.items() if v.isalpha() and v.islower()}
    start = [k for k,v in grid.items() if '@' in v]
    return grid, keys, start

def trace_steps(grid, pos, visited=[], paths={}, steps=0):
    doors = []
    move = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while set(visited) != set(grid.keys()):
        val = grid[pos]
        if val.isalpha() and val.islower():
            paths[val] = {'steps': steps, 'doors': set(doors)}
        elif val.isalpha() and val.isupper():
            doors.append(val.lower())
        visited.append(pos)

        possible_paths = [(pos[0] + dx, pos[1] + dy) for dx, dy in move]
        possible_paths = [p for p in possible_paths if p in grid.keys() and p not in visited]

        if not possible_paths:
            return paths, visited
        elif len(possible_paths) == 1:
            steps += 1
            pos = possible_paths[0]
        else:
            for new_pos in possible_paths:
                paths, visited = trace_steps(grid, new_pos, visited, paths, steps + 1)

    return paths, visited

def find_nodes(keypaths, current_node='@0', path=[], steps=0):
    while len(path) != len(keypaths.keys()):
        path.append(current_node)
        possible_paths = [k for k, v in keypaths[current_node].items() if k != current_node and k not in path and v['doors'].difference(set(path)) == set()]
        print(current_node, path, possible_paths, steps)

        if not possible_paths:
            return steps, path
        elif len(possible_paths) == 1:
            node = possible_paths[0]
        else:  # use recursion to determine best of multiple steps
            all_steps = {poss_node: find_nodes(keypaths, poss_node, path.copy(), steps)[0] for poss_node in possible_paths}
            node = [k for k, v in all_steps.items() if v == min(all_steps.values())][0]

        steps += keypaths[current_node][node]['steps']
        current_node = node

    return steps, path

if __name__ == '__main__':
    _input = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''.splitlines()
#     _input = '''########################
# #...............b.C.D.f#
# #.######################
# #.....@.a.B.c.d.A.e.F.g#
# ########################'''.splitlines()
#     _input = '''#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################'''.splitlines()
    _input = '''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''.splitlines()
    grid, keys, starts = parse_grid(_input)
    keypaths = {key: trace_steps(grid, key_pos, visited=[], paths={}, steps=0)[0] for key, key_pos in keys.items()}

    for start in range(len(starts)):
        keypaths['@' + str(start)] = trace_steps(grid, starts[start], visited=[], paths={}, steps=0)[0]

    print('completed keypaths:', keypaths)
    steps, path = find_nodes(keypaths, current_node='@0', path=[], steps=0)
    print(f'number of steps: {steps}, path: {" ".join(path)}')

