from _utils import read_input, timer

from collections import defaultdict
from itertools import permutations

import heapq


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


def manhattan_distance(coord1, coord2):
    """
    Takes in 2 tuples of coordinates & returns their Manhattan Distance
    (sum of absolute value of the differences).
    :param coord: tuple[int], tuple[int]
    :return: int
    """
    dist = [abs(c1 - c2) for c1, c2 in zip(coord1, coord2)]
    return sum(dist)


def find_transform(coords1: list, coords2: list):
    """
    Returns the transformation function that turns coordinates
    from coords2 into coordinates of coords1.

    This uses the fact that coords1 and coords2 are beacons
    that both scanners have in common, identified earlier using
    a distance fingerprint, so we *know* the correct transform
    will map all 12 beacons from one system to another.
    """
    all_perms = permutations([0, 1, 2])
    signs = [
        (x, y, z)
        for x in range(-1, 2)
        for y in range(-1, 2)
        for z in range(-1, 2)
        if x != 0 and y != 0 and z != 0
    ]

    for perm in all_perms:
        i, j, k = perm
        for sign in signs:
            prev_vector = None
            counter = 1
            for c1, c2 in zip(coords1, coords2):
                vector = tuple([c1[r] - c2[perm[r]] * sign[perm[r]] for r in range(3)])

                if not prev_vector:
                    prev_vector = vector
                elif prev_vector != vector:
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


def map_distances(lst: list):
    distances = {}

    for coords1 in lst:
        distances[coords1] = [manhattan_distance(coords1, coords2) for coords2 in lst]

    return distances


def find_common_beacons(d1: dict, d2: dict):
    """
    Find overlapping beacons between 2 scanners.
    Scanners will always have an overlap of 12 beacons.

    This uses the fact that beacons will have the same distance
    to another beacon regardless of the transformation applied by
    the scanner - the rule of thumb is at least 11 of the distances
    between a beacon observed by 2 different scanners will match.
    (11 if 2 points are at same distance from beacon, 13 bc we include
    distance from beacon to itself).
    """
    common_beacons1 = []
    common_beacons2 = []

    for coords1, coords1_distances in d1.items():
        for coords2, coords2_distances in d2.items():
            coords1_distances = set(coords1_distances)
            coords2_distances = set(coords2_distances)

            if len(coords1_distances.intersection(coords2_distances)) >= 11:
                common_beacons1.append(coords1)
                common_beacons2.append(coords2)

    return (
        common_beacons1,
        common_beacons2,
    )


def find_overlapping_scanners(distance_dict: dict, MAX_IX: int):
    path = defaultdict(list)
    trans_funcs = {}
    rel_scanner_positions = {}
    for i in range(MAX_IX):
        for j in range(i + 1, MAX_IX):
            (
                cb1,
                cb2,
            ) = find_common_beacons(distance_dict[i], distance_dict[j])
            if cb1 and cb2:
                path[i].append(j)
                path[j].append(i)

                trans_func, scanner_position = find_transform(cb1, cb2)
                reverse_trans_func, reverse_scanner_position = find_transform(cb2, cb1)

                trans_funcs[(j, i)] = trans_func  # trans func from j to i
                trans_funcs[(i, j)] = reverse_trans_func  # trans func from j to i

                rel_scanner_positions[(j, i)] = scanner_position
                rel_scanner_positions[(i, j)] = reverse_scanner_position

    return path, trans_funcs, rel_scanner_positions


def translate_coordinates(
    scanners: dict,
    rel_scanner_positions: dict,
    path: dict,
    trans_funcs: dict,
    MAX_IX: int,
):
    all_translations = {k: set(v) for k, v in scanners.items()}

    scanner_pos = defaultdict(set)
    for k, v in rel_scanner_positions.items():
        scanner_pos[k[1]].add(tuple(v))

    for k in range(1, MAX_IX):
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
                        translated_positions = set(
                            map(trans_funcs[(node, new_node)], scanner_pos[node])
                        )
                        if translated_positions:
                            scanner_pos[new_node] = scanner_pos[new_node].union(
                                translated_positions
                            )

                        heapq.heappush(queue, (steps, new_node))

    return all_translations, scanner_pos


def max_distance(lst):
    """
    Returns maximum distance between 2 points.
    """
    max_d = 0
    for ix, coords1 in enumerate(lst):
        for jx, coords2 in enumerate(lst):
            d = manhattan_distance(coords1, coords2)
            max_d = max(d, max_d)

    return max_d


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    scanners = parse_input(_input)
    MAX_IX = 1 + max(scanners.keys())

    # get all distances within scanner coords
    distance_dict = {}
    for key, val in scanners.items():
        distance_dict[key] = map_distances(val)

    # find scanners in common using distances
    path, trans_funcs, rel_scanner_positions = find_overlapping_scanners(
        distance_dict, MAX_IX
    )

    # translate all scanner & beacon coordinates
    all_translations, scanner_pos = translate_coordinates(
        scanners, rel_scanner_positions, path, trans_funcs, MAX_IX
    )

    part_1_score = len(all_translations[0])
    part_2_score = max_distance(scanner_pos[0])

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc19.txt")
    print(f"PART 1: {part_1_score}")  # 392
    print(f"PART 2: {part_2_score}")  # 13332
