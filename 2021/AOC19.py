from _utils import read_input, timer

from collections import defaultdict
from itertools import permutations


def find_transform(coords1: list, coords2: list):
    perms = permutations([0, 1, 2])
    signs = [
        (x, y, z)
        for x in range(-1, 2)
        for y in range(-1, 2)
        for z in range(-1, 2)
        if x != 0 and y != 0 and z != 0
    ]

    for curr_perm in perms:
        i, j, k = curr_perm
        for sign in signs:
            vector = None
            counter = 1
            for ix in range(len(coords1)):
                c1 = coords1[ix]
                c2 = coords2[ix]
                tr_c2 = c2[i] * sign[i], c2[j] * sign[j], c2[k] * sign[k]
                new_abs_val_vector = [c1[i] - tr_c2[i] for i in range(3)]

                if not vector:
                    vector = new_abs_val_vector
                elif new_abs_val_vector != vector:
                    break
                else:
                    counter += 1

                if counter == 12:
                    trans_func = lambda x: (
                        x[i] * sign[i] + vector[0],
                        x[j] * sign[j] + vector[1],
                        x[k] * sign[k] + vector[2],
                    )
                    return trans_func, vector
    return None, None


def parse_input(_input: list):
    scanners = defaultdict(list)

    for line in _input:
        if "scanner" in line:
            scanner_num = line.split("--- scanner ")[1]
            scanner_num = int(scanner_num.replace("---", ""))

        elif "," in line:
            coords = map(int, line.split(","))
            x, y, z = coords
            scanners[scanner_num].append((x, y, z))

    return scanners


def manhattan_distance(coord1, coord2, p=False):
    """Takes in 2 tuples of coordinates (x, y, z), returns
    Manhattan Distance (sum of absolute value of the coordinates).

    :param coord: tuple[int], tuple[int]
    :return: int
    """
    coord1 = [-x for x in coord1]
    zipped = zip(coord1, coord2)
    dist = [abs(sum(t)) for t in zipped]
    return sum(dist)


def map_distances(lst: list):
    distances = {}

    for ix, coords1 in enumerate(lst):
        all_d = []
        for jx, coords2 in enumerate(lst):
            d = manhattan_distance(coords1, coords2)
            all_d.append(d)

        distances[coords1] = all_d

    return distances


def find_common_beacons(d1: dict, d2: dict):
    common_beacons1 = []
    common_beacons2 = []
    counter = 0
    for coords1, coords1_distances in d1.items():
        for coords2, coords2_distances in d2.items():
            coords1_distances = set(coords1_distances)
            coords2_distances = set(coords2_distances)

            if len(coords1_distances.intersection(coords2_distances)) >= 11:
                common_beacons1.append(coords1)
                common_beacons2.append(coords2)
                counter += 1

    transform_func, scanner_position = find_transform(common_beacons1, common_beacons2)
    reverse_transform_func, reverse_scanner_position = find_transform(common_beacons2, common_beacons1)
    return (
        common_beacons1,
        common_beacons2,
        counter,
        transform_func,
        reverse_transform_func,
        scanner_position,
        reverse_scanner_position
    )


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    scanners = parse_input(_input)

    # get all distances within scanner coords
    print('read input')
    distance_dict = {}
    for key, val in scanners.items():
        distance_dict[key] = map_distances(val)

    # find scanners in common using distances
    print('find scanners')
    path = defaultdict(list)
    trans_funcs = {}
    rel_scanner_positions = {}
    MAX_IX = 1 + max(scanners.keys())
    for i in range(MAX_IX):
        for j in range(i + 1, MAX_IX):
            cb1, cb2, counter, trans_func, reverse_trans_func, scanner_position, reverse_scanner_position = find_common_beacons(
                distance_dict[i], distance_dict[j]
            )
            if counter == 12:
                path[i].append(j)
                path[j].append(i)

                rel_scanner_positions[(j, i)] = scanner_position
                rel_scanner_positions[(i, j)] = reverse_scanner_position

                trans_funcs[(j, i)] = trans_func  # trans func from j to i
                trans_funcs[(i, j)] = reverse_trans_func  # trans func from j to i

    import heapq
    print('translate everything')
    all_translations = {k: set(v) for k, v in scanners.items()}
    scanner_pos = defaultdict(list)
    for k, v in rel_scanner_positions.items():
        scanner_pos[k[1]].extend([v])

    for k in range(1, MAX_IX):
        print(f"translating {k} out of {MAX_IX}")
        queue = []
        heapq.heappush(queue, (0, k))
        visited = set()

        while queue:
            steps, node = heapq.heappop(queue)
            steps += 1
            visited.add(node)

            if node == 0 or 0 in visited:
                queue = []
            else:
                next_nodes = path[node]

                for new_node in next_nodes:
                    if new_node not in visited:
                        translated = set(
                            map(trans_funcs[(node, new_node)], all_translations[node])
                        )
                        all_translations[new_node] = all_translations[new_node].union(
                            translated
                        )
                        translated_positions = list(
                            map(trans_funcs[(node, new_node)], scanner_pos[node])
                        )
                        if translated_positions:
                            scanner_pos[new_node].extend(
                                        translated_positions
                            )

                        heapq.heappush(queue, (steps, new_node))

    part_1_score = len(all_translations[0])
    print(f'part 1: {part_1_score}')

    lst = scanner_pos[0]
    max_d = 0
    for ix, coords1 in enumerate(lst):
        for jx, coords2 in enumerate(lst):
            d = manhattan_distance(coords1, coords2)
            max_d = max(d, max_d)

    part_2_score = max_d

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc19.txt")
    print(f"PART 1: {part_1_score}")  # 392
    print(f"PART 2: {part_2_score}")  # .
