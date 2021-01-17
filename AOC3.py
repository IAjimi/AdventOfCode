def sloped_collision_count(_input, x, y):
    '''
    x is rightward movement, y is downward movement.

    The x-axis position of the skier is determined by the current row we are at, 
    the speed of descent x/y, and the length of the input. 
    Since the same map is reproduced ad-infinitum, we need to get the reminder of the division of the 
    x-axis location by the length of the array.

    i % y == 0 is a check mostly implemented for the case where downward movement != 1 (it is always true
    when y == 1) to skip the rows the skier does not go through / stop at.
    '''
    collisions = [e[int( (i*x/y) % len(_input[i]) )] for i,e in enumerate(_input) if i >= 1 and i % y == 0]
    collisions = [1 if i == '#' else 0 for i in collisions]
    return sum(collisions)

def testing_out_slopes(slope_combinations):
    solution = 1

    for x,y in slope_combinations:
        collisions = slope_collision_count(_input, x, y)
        solution = solution * collisions

    return solution

if __name__ == "__main__":
    _input = open("aoc_3.txt").read().splitlines()
    
    print("PART 1")
    sloped_collision_count(_input, 3, 1)
    print("")
    print("PART 2")
    slope_combinations = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    testing_out_slopes(slope_combinations)