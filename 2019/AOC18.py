'''Runs fairly slowly for part 1, issue being the use of recursion with multiple possible steps at once.

1) grid only keeps points of interest (starts, keys, doors)
2) keypaths keeps distance from start/key to key, with doors needed to unlock the path
-> not done optimally: scans the whole space for every key, even though reciprocity of distance
means only need to do it 1x by pair
3) uses recursion to generate path, keeping optimal (min distance) point only
-> ends up being very slow for real input
'''

import time


def parse_grid(_input):
    grid = {
        (x, y): _input[y][x]
        for y in range(len(_input))
        for x in range(len(_input[y]))
        if _input[y][x] != "#"
    }
    keys = {v: k for k, v in grid.items() if v.isalpha() and v.islower()}
    start = [k for k, v in grid.items() if "@" in v]
    return grid, keys, start


def update_grid(grid, start):
    x, y = start

    # Turn into wall
    new_walls = [(x, y), (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    for w in new_walls:
        if w in grid:
            del grid[w]

    # Add new starts
    new_starts = [(x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1)]
    for s in new_starts:
        grid[s] = "@"

    return grid, new_starts


def calc_len_path(path):
    steps = [keypaths[path[i]][path[i + 1]]["steps"] for i in range(0, len(path) - 1)]
    return sum(steps)


def trace_steps(grid, pos, visited=[], destinations={}, steps=0):
    """This walks through the whole grid to calculate distance
    between keys and starting points. Would be more efficient to iterate
    over letters to take advantage of the fact that distance from a to b = distance from b to a."""
    doors = []
    move = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    while set(visited) != set(grid.keys()):
        val = grid[pos]
        if val.isalpha() and val.islower():
            destinations[val] = {"steps": steps, "doors": set(doors)}
        elif val.isalpha() and val.isupper():
            doors.append(val.lower())
        visited.append(pos)

        possible_paths = [(pos[0] + dx, pos[1] + dy) for dx, dy in move]
        possible_paths = [
            p for p in possible_paths if p in grid.keys() and p not in visited
        ]

        if not possible_paths:
            return destinations
        elif len(possible_paths) == 1:
            steps += 1
            pos = possible_paths[0]
        else:
            for new_pos in possible_paths:
                destinations = trace_steps(
                    grid, new_pos, visited, destinations, steps + 1
                )

    return destinations


def get_keypaths(grid, keys, starts):
    keypaths = {
        key: trace_steps(grid, key_pos, visited=[], destinations={}, steps=0)
        for key, key_pos in keys.items()
    }

    for start in range(len(starts)):
        keypaths["@" + str(start)] = trace_steps(
            grid, starts[start], visited=[], destinations={}, steps=0
        )

    return keypaths


def find_nodes(keypaths, cache, current_node="@0", found_keys=set(), path=[]):
    while len(found_keys) != len(keypaths.keys()):
        if current_node not in path:
            path.append(current_node)
            found_keys.add(current_node)

        possible_paths = [
            k
            for k, v in keypaths[current_node].items()
            if k not in found_keys and v["doors"].difference(found_keys) == set()
        ]

        if not possible_paths or len(found_keys) == len(keypaths.keys()):
            return path
        elif len(possible_paths) == 1:
            node = possible_paths[0]
        else:  # use recursion to determine best of multiple steps
            all_steps = []
            missing_keys = "".join(set(keypaths.keys()).difference(found_keys))

            for poss_node in possible_paths:
                cachekey = poss_node + missing_keys

                if cachekey in cache:
                    new_steps = cache[cachekey]
                else:
                    new_path = find_nodes(
                        keypaths,
                        cache,
                        poss_node,
                        found_keys.copy(),
                        path.copy(),
                    )
                    new_steps = calc_len_path(new_path)
                    cache[cachekey] = new_steps

                all_steps.append(new_steps)

            node = possible_paths[all_steps.index(min(all_steps))]

        current_node = node

    return path

def bot_collection(keypaths, starts):
    cache = {}
    found_keys = set()
    bot_path = {"@" + str(start): [] for start in range(len(starts))}

    while set(keypaths.keys()).difference(set(found_keys)) != set():
        for start in range(len(starts)):
            s = "@" + str(start)
            possible_paths = [
                k
                for k, v in keypaths[s].items()
                if k not in found_keys
                and v["doors"].difference(found_keys) == set()
            ]
            if possible_paths:
                path = bot_path[s]
                new_path = find_nodes(
                    keypaths,
                    cache=cache,
                    current_node=s,
                    found_keys=found_keys,
                    path=path.copy(),
                )
                bot_path[s] = new_path
                print(s, bot_path[s])
                for n in new_path:
                    found_keys.add(n)
        print('\n')

    all_paths = [v for k, v in bot_path.items()]
    total_steps = sum([calc_len_path(p) for p in all_paths if len(p) >= 2])
    return total_steps

if __name__ == "__main__":
    _input = open("aoc18.txt").read().splitlines()
    grid, keys, starts = parse_grid(_input)

    t0 = time.time()
    keypaths = get_keypaths(grid, keys, starts)
    t1 = round(time.time() - t0, 2)
    print(f"completed keypaths, speed: {t1}")  # 30 sec!

    t0 = time.time()
    path = find_nodes(keypaths, cache={}, current_node="@0", found_keys=set(), path=[])  # 4246
    t1 = round(time.time()-t0, 2)
    print(f'PART 1: number of steps: {calc_len_path(path)}, path: {" ".join(path)}, speed: {t1}')

    # PART 2
    t0 = time.time()
    _input = open("2019/aoc18.txt").read().splitlines()
    grid, keys, starts = parse_grid(_input)
    grid, starts = update_grid(grid, starts[0])
    keypaths = get_keypaths(grid, keys, starts)
    sol2 = bot_collection(keypaths, starts)
    t1 = round(time.time() - t0, 2)
    print(f"total steps: {sol2}, speed: {t1}")  # 1940, +-5.63 sec total
