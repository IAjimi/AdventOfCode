''' Took me a minute to get there conceptually (confusing example). The key
is to realize that 1) the space is infinite 2) only neighbors of cubes matter.
This starts with the initial board, expands it to all neighbors of active cubes 
on the initial board, actives / deactivates cubes, repeats.

Switch from part 1 to part 2 relies on dim4 parameter, which mostly changes
get_neighbors_positions. That modification trickles down to the rest of the code.

Runs in <1 second for part 1. Takes 5min for part 2.'''

def get_neighbors_positions(i,j,k,l, dim4 = False):
    '''Gets the position of neighbors for any given cube. '''
    if dim4 == True:
        neighbor_positions = [(i+a, j+b, k+c, l+d) for a in range(-1,2) for b in range(-1,2) for c in range(-1,2) for d in range(-1,2)]
    else:
        neighbor_positions = [(i+a, j+b, k+c, 0) for a in range(-1,2) for b in range(-1,2) for c in range(-1,2)]

    neighbor_positions = [v for v in neighbor_positions if v != (i,j,k,l)]
    
    return neighbor_positions

def count_neighbors_active(current_plane, neighbors, k):
    ''' Counts the number of active neighbors.
    Only looks at neighbors in the current plane, since those outside are all inactive.'''
    neigh = neighbors[k]
    active_neighbors = [current_plane[v] for v in neigh if v in current_plane.keys()]
    return active_neighbors.count('#')

def expand_plane(current_plane, neighbors, dim4 = False):
    ''' Expand the plane to add neighbors that might be affected (turned into cubes) 
    during iteration. Because inactive cubes can only be changed by active cubes,
    this only adds neighbors of active cubes.'''
    current_keys = list(current_plane.keys())

    for k in current_keys:
        neigh = neighbors[k]
        val = current_plane[k]
        
        if val == '#':
            for n in neigh:
                if n not in current_keys:
                    current_plane[n] = '.'
                    neighbors[n] = get_neighbors_positions(n[0],n[1],n[2],n[3], dim4)

    return current_plane, neighbors

def cube_activation(current_plane, dim4):
    '''Iterates through the expanded version of the current plane. 
    Stores the new status of every cube (active or inactive) into a 
    new plane. '''
    new_plane = {}
    neighbors = {k:get_neighbors_positions(k[0], k[1], k[2], k[3], dim4) for k in current_plane.keys()}
    current_plane, neighbors = expand_plane(current_plane, neighbors, dim4)

    for k,v in current_plane.items():
        neigh = count_neighbors_active(current_plane, neighbors, k)

        if v == '#' and neigh not in [2, 3]:
            new_plane[k] = '.'
        elif v == '.' and neigh == 3:
            new_plane[k] = '#'
        else:
            new_plane[k] = v

    return new_plane

def count_cubes(_input, dim4):
    '''Initializes the process with the first current plane, then
    simulates 6 rounds of expansion.'''

    # Get Values on Current Input, setting z = 0
    current_plane = {(i,j,0,0):_input[i][j] for i in range(len(_input)) for j in range(len(_input[0]))}

    # Simulate 6 rounds
    n = 0

    while n < 6:
        n += 1
        current_plane = cube_activation(current_plane, dim4)
        print( list(current_plane.values()).count('#') )

    return list(current_plane.values()).count('#')

if __name__ == "__main__":
    _input = open("aoc_17.txt").read().splitlines()
    
    print("PART 1")
    count_cubes(_input, dim4 = False)
    print("")
    print("PART 2")
    count_cubes(_input, dim4 = True)


