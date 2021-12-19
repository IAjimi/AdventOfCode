from _utils import read_input, timer

from collections import defaultdict
from itertools import permutations

def find_transform(coords1:list, coords2:list):
    perms = permutations([0,1,2])
    signs = [(x,y,z) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2) if x != 0 and y != 0 and z != 0]

    for i,j,k in perms:
        for sign in signs:
            transform = None
            counter = 1
            for ix in range(len(coords1)):
                c1 = coords1[ix]
                c2 = coords2[ix]
                tr_c2 = c2[i] * sign[0], c2[j] * sign[1], c2[k] * sign[2]
                new_transform = [c1[i] - tr_c2[i] for i in range(3)]
                if not transform:
                    transform = new_transform
                elif new_transform != transform:
                    break
                else:
                    counter +=1

                if counter == 12:
                    return transform

    return None


def parse_input(_input:list):
    scanners = defaultdict(list)

    for line in _input:
        if "scanner" in line:
            scanner_num = line.split("--- scanner ")[1]
            scanner_num = int(scanner_num.replace("---", ""))

        elif "," in line:
            coords = map(int, line.split(","))
            # x,y = coords
            # scanners[scanner_num].append((x,y))
            x,y,z = coords
            scanners[scanner_num].append((x,y,z))

    return scanners


def manhattan_distance(coord1, coord2, p=False):
    ''' Takes in 2 tuples of coordinates (x, y, z), returns
    Manhattan Distance (sum of absolute value of the coordinates).

    :param coord: tuple[int], tuple[int]
    :return: int
    '''
    coord1 = [-x for x in coord1]
    zipped = zip(coord1, coord2)
    dist = [abs(sum(t)) for t in zipped]
    if p: print(dist)
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

def find_common_beacons(d1:dict, d2:dict):
    common_beacons1 = []
    common_beacons2 = []
    counter = 0
    for coords1,coords1_distances in d1.items():
        for coords2, coords2_distances in d2.items():
            coords1_distances = set(coords1_distances)
            coords2_distances = set(coords2_distances)

            if len(coords1_distances.intersection(coords2_distances)) >= 11:
                common_beacons1.append(coords1)
                common_beacons2.append(coords2)
                #d1_to_d2_vector = vector(coords1, coords2)
                counter +=1

    tr = find_transform(common_beacons1, common_beacons2)
    return common_beacons1, common_beacons2, counter, tr


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    scanners = parse_input(_input)

    # get all distances within scanner coords
    distance_dict = {}
    for key, val in scanners.items():
        distance_dict[key] = map_distances(val)
    # find scanners in common using distances
    MAX_IX = 1 + max(scanners.keys())
    for i in range(MAX_IX):
        for j in range(i + 1, MAX_IX):
            cb1, cb2, counter, tr = find_common_beacons(distance_dict[i], distance_dict[j])
            print(i, j, counter, tr)

    import pdb; pdb.set_trace()

    part_1_score = 0
    part_2_score = 0
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("test_aoc19.txt")
    print(f"PART 1: {part_1_score}")  # .
    print(f"PART 2: {part_2_score}")  # .
