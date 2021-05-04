''' In Part 1, the bottom right of every square is the series of odd numbers squared. The length
of the square with bottom corner n**2 is n - 1.

To get the distance from (1), we subtract from the length the remainder of the difference of the number
from the bottom right corner of its square divided by the length of the square.

For example, 16 is between 9 and 25, so it belongs to the square with 25 at the bottom right corner.
There is a difference of 9 between 16 and 25. The remainder of this difference divided by the length
of the side of the square tells us the position of 16 on the edge of the square it belongs to.

In this case, 17 is position 0, 16 is position 1, 15 is position 2, 14 is position 3, and 13 is position 4.

We subtract the position of the number from the length of the edge. This value is 4 for 17, 3 for 15,
2 for 15, 1 for 14, and 0 for 13. This is only correct for the first half of the the edge
(position < max_position / 2). We correct this calculation for the second half by subtracting this
value from the length of the edge.

Sample square:
#  37  36  35  34  33  32  31
#  38  17  16  15  14  13  30
#  39  18   5   4   3  12  29
#  40  19   6  (1)  2  11  28
#  41  20   7   8   9  10  27
#  42  21  22  23  24  25  26
#  43  44  45  46  47  48  49

Sample distance:
#   6   5   4   3   4   5   6
#   5   4   3   2   3   4   5
#   4   3   2   1   2   3   4
#   3   2   1  (0)  1   2   3
#   4   3   2   1   2   3   4
#   5   4   3   2   3   4   5
#   6   5   4   3   4   5   6

'''

import numpy as np

def find_steps(num):
    if num == 1:
        return 1

    _sq = round(np.sqrt(num) - 0.5)

    if _sq % 2 == 0:
        _min = _sq - 1
        _max = _sq + 1
    else:
        _min = _sq
        _max = _sq + 2

    length = _max - 1

    steps = length - ((_max - num) % length)
    if steps < length / 2:
        steps = length - steps

    return steps

def get_positions(r):
    # need to build the corners in order
    right_corner = [(r, w) for w in range(1-r, r+1)]
    top_corner = [(w, r) for w in range(r-1, -r-1, -1)]
    left_corner = [(-r, w) for w in range(r-1, -r-1, -1)]
    bottom_corner = [(w, -r) for w in range(1-r, r+1)]
    positions = right_corner + top_corner + left_corner + bottom_corner
    return positions

def iterate_square(n):
    found = False
    r, val = 1, 1
    grid = {(0, 0): 1}
    neighbors = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    while not found:
        positions = get_positions(r)
        for p in positions:
            adj_positions = [(p[0] + v[0], p[1] + v[1]) for v in neighbors]
            val = sum([grid[v] for v in adj_positions if v in grid.keys()])

            if val > n:
                return val
            else:
                grid[p] = val

        r += 1

if __name__ == "__main__":
    sol1 = find_steps(368078)  # 371
    sol2 = iterate_square(368078)  # 369601
    print(f'PART 1: {sol1} \n PART 2: {sol2}')



