def find_earliest_timestamp(bus_id, target_time):
    if target_time % bus_id != 0:
        s = (target_time // bus_id) + 1
        return bus_id * s
    else:
        return target_time

def find_right_bus(bus_ids, target_time):
    earliest_times = list(map(find_earliest_timestamp, bus_ids, [target_time for b in bus_ids]))
    best_bus_id = bus_ids[earliest_times.index(min(earliest_times))]
    wait_time = (min(earliest_times) - target_time) * best_bus_id
    return wait_time

def product(_list):
    ''' Simple multiplication function to replace np.prod. '''
    res = 1
    
    for l in _list:
        res = res * l
    
    return res

def chinese_remainder_theorem(bus_ids, offset):
    '''Non obvious solution. I initially tried finding the intersection
    of the 'lines' created by each bus, then matching remainders to the unique
    remainder signature that would be created by the timestamp.

    Ultimately looked up some AoC threads to get some ideas. Saw the Chinese
    Remainder Theorem being mentioned, which led me to the page quote below,
    and this function / solution.

    Source: http://homepages.math.uic.edu/~leon/mcs425-s08/handouts/chinese_remainder.pdf

    This initially used numpy for element-wise multiplication but np couldn't handle
    the size of the integers used, so I had to revert to doing this with list comprehension.

    bus_ids: Equivalent of a list of modulos m1, m2, ..., mn
    z: List of z1 = m / m1, z2 = m / m2, etc where m is the product of all m in bus_ids
    y: List of inverses of z, i.e., y = inverse(z1) (mod m1), etc
    w: Product of y * z

    Returns the unique solution % m.
    '''

    a = [bus_ids[n] - offset[n] if offset[n] > 0 else 0 for n in range(len(bus_ids))]
    a = [(bus_ids[n] - offset[n]) % bus_ids[n] if offset[n] > 0 else 0 for n in range(len(bus_ids))]
    y, z = [], []

    for m in bus_ids:
        other_modulo = [i for i in bus_ids if i != m]
        zm = product(other_modulo)

        # Looking for ym, the inverse of zm % m
        inverse = zm % m
        remainder = [r for r in range(m) if (inverse * r) % m == 1]

        z.append(zm)
        y.append(remainder[0])

    w = [z[n] * y[n] for n in range(len(y))]
    manual_sum = sum([w[n] * a[n] for n in range(len(w))])

    return manual_sum % product(bus_ids)


if __name__ == "__main__":
    _input = open("aoc_13.txt").read().splitlines()

    target_time = int(_input[0])
    bus_ids = [int(num) for num in _input[1].split(',') if num != 'x']
    offset = [ix for ix, num in enumerate(_input[1].split(',')) if num != 'x']
    
    print("PART 1")
    find_right_bus(bus_ids, target_time)
    print("")
    print("PART 2")
    chinese_remainder_theorem(bus_ids, offset)


