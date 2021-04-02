from collections import Counter

def get_location(string):
    ''' Got hex grid system from stack overflow:
    https://math.stackexchange.com/questions/2254655/hexagon-grid-coordinate-system'''
    north, east = 0, 0
    directions = {'se': (0,1), 'sw':(-1,1), 'nw':(0,-1), 'ne':(1,-1), 'e':(1,0), 'w':(-1,0)}

    for d,v in directions.items():
    	# Count Number of Occurences of Direction
        n = string.count(d)

        # Remove Direction from String
        string = string.replace(d, '')

        # Update Position
        north += n * v[0]
        east += n * v[1]

    return (north, east)

def get_black_tiles(_input):
	# Get Locations for Every Line
	tile_locations = [get_location(s) for s in _input]

	# Count Number of Flips per Tile 
	flip_count = dict(Counter(tile_locations))

	return flip_count

def count_flips_to_black(_input):
	# Count Number of Flips per Tile 
	flip_count = get_black_tiles(_input)
	flip_count = list(flip_count.values())

	# Odd number of flip = black tile
	black_tiles = sum([1 for v in flip_count if v % 2 != 0])

	return black_tiles

def get_neighbors(position, tiles_color_map):
    neighbors = []
    directions = [(0,1), (-1,1), (0,-1), (1,-1), (1,0), (-1,0)]

    for d in directions:
        pos1 = position[0] + d[0]
        pos2 = position[1] + d[1]
        neighbors.append((pos1, pos2))

    return neighbors

def expand_neighbors(tiles_color_map):
    ''' Part 2 requires us to consider all tiles that are near black tiles. By default, 
    those are white. 

    This gets all neighbors of black tiles and adds them to our tiles_color_map dict.'''
    
    # Get neighbors of black tiles
    new_tiles = [get_neighbors(k, tiles_color_map) for k,v in tiles_color_map.items() if v == 1]
    new_tiles = [item for sublist in new_tiles for item in sublist] # flatten
    
    # Add them to tiles_color_map
    for t in set(new_tiles):
        if t not in tiles_color_map.keys():
            tiles_color_map[t] = 0
            
    # Return new dict of neibhors
    neighbors_dict = {k:get_neighbors(k, tiles_color_map) for k in tiles_color_map.keys()}
    
    return neighbors_dict

def living_art_exhibit(_input):
	# Get Black Tiles, Store in Dict
	flip_count = get_black_tiles(_input)
	tiles_color_map = {k:1 if v % 2 != 0 else 0 for k,v in flip_count.items()}

	for _ in range(100):
		# First, Need to Expand Tile Universe
	    neighbors_dict = expand_neighbors(tiles_color_map)
	    
	    # Set Copy of Dict that we can modify
	    new_tiles_color_map = tiles_color_map.copy()

	    # For every tile, get # of adj black tiles & change color accordingly
	    for pos,color in tiles_color_map.items():
	        adj_black_tiles = 0
	        neighbors = neighbors_dict[pos]

	        for n in neighbors:
	            if n in tiles_color_map.keys():
	                adj_black_tiles += tiles_color_map[n]

	        if (color == 1) & (adj_black_tiles == 0):
	            new_tiles_color_map[pos] = 0
	        elif (color == 1) & (adj_black_tiles > 2):
	            new_tiles_color_map[pos] = 0
	        elif (color == 0) & (adj_black_tiles == 2):
	            new_tiles_color_map[pos] = 1

	    tiles_color_map = new_tiles_color_map
	    
    # Compute # of Black Tiles
    black_count = sum(list(tiles_color_map.values()))
    
    return black_count

if __name__ == "__main__":
    _input = open("aoc_24.txt").read().splitlines()
    
    print("PART 1")
    print(count_flips_to_black(_input)) # 354
    print("")
    print("PART 2")
    print(living_art_exhibit(_input)) # 3608