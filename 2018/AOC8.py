# Used https://0xdf.gitlab.io/adventofcode2018/#day-8 as guide

def walk_tree(_input):
    tree = {}
    n_child = _input.pop(0)
    n_metadata = _input.pop(0)
    meta = 0
    value = 0
    
    # Get sum of metadata for part 1 and 
    # update tree w/ child number and metadata value for part 2
    for n in range(n_child):
        new_meta, tree[n] = walk_tree(_input)
        meta += new_meta
        
    # Update metadata sum for part 1, for part 2 update value
    # retrieving relevant child metadata sum using the tree dict
    for n in range(n_metadata):
        new_meta = _input.pop(0)
        meta += new_meta
        
        if new_meta - 1 in tree.keys():
            value += tree[new_meta - 1]
        
    # If no children the value of the node = the sum of its metadata
    if n_child == 0:
        value += meta
        
    return meta, value

if __name__ == "__main__":
	_input = open("aoc_8.txt").read().split()
    _input = [int(i) for i in _input]

	sol1, sol2 = walk_tree(_input) # 48155, 40292
    print('PART 1: {} \n PART 2: {}'.format(sol1, sol2))