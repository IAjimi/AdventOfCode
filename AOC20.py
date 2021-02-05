def parse_tile(string):
    ''' Takes in raw tile string, returns tile id + the tile's 4 edges
    in a list.'''
    tile_id = string.split(':\n')[0].split(' ')[1]
    raw_tiles = string.split(':\n')[1].splitlines()

    edges = [raw_tiles[0]] + [raw_tiles[-1]] # top and bottom edge of original tile
    left_edge = ''.join([t[0] for t in raw_tiles]) # left side of original tile
    right_edge = ''.join([t[-1] for t in raw_tiles]) # right side
    edges += [left_edge] + [right_edge]

    return tile_id, edges

def find_corners(tiles):
    ''' Takes in a dictionary of tile_id:[tile_edges],
    outputs product of corner tile ids.

    The current tile is taken as is. All other tile edges are
    considered, including flipped. I iterate over the current 
    tile's edges to find matches. Matches are unique, so this is ok.
    Probably not super efficient, since match + 1 implies I've
    found another tile's match as well.

    Corners (by definition) only have 2 matches, so finding the
    product of tile id is fairly easy.'''

    product = 1

    for tile_id, current_tiles in tiles.items():
        match = 0
        
        # Add Tiles from Other Keys
        other_tiles = [v for k,v in tiles.items() if k != tile_id]
        other_tiles = [item for sublist in other_tiles for item in sublist] # flattened
        other_tiles += [t[::-1] for t in other_tiles]
        
        for tile in current_tiles:
            if tile in other_tiles: 
                match += 1
        
        if match == 2: 
            product = product * int(tile_id)

    return product
 
if __name__ == "__main__":
    _input = open("aoc_20.txt").read().split('\n\n')
    tiles = dict(map(parse_tile, _input))
    
    print("PART 1")
    find_corners(tiles)
    print("")
    print("PART 2")


