'''Might want to refactor this. Took great care in part 1 to create code that
could create binary strings. Ultimately, all that matters is the position of 1s
in the number and 0s & 1s in the mask, which is the approach taken in part 2.'''

from itertools import combinations

def num_to_binary(num):
    bit = []
    done = False

    while not done:
        bit.append(num % 2)

        if num // 2 == 0: 
            done = True
        else:
            num = num // 2

    bit = [b for b in bit][::-1] # chars to string + reverse sequence
    bit = [0 for r in range(36 - len(bit))] + bit # pad with 0s
    
    return bit

def binary_to_num(bit):
    num = [2**(35-ix) for ix,val in enumerate(bit) if val != 0]
    return sum(num)

def mask_overwrite(num, mask):
    ''' Applies the mask overwrite of part 1. Returns a single number.'''
    bit = num_to_binary(num)
    
    for ix, val in mask:
        bit[ix] = val
    
    return binary_to_num(bit)

def initalize_program(_input):
    memory_dict = {}

    for instruc in _input:
        if 'mask' in instruc:
            # Retrieve Mask
            mask = instruc.split(' = ')[1]
            mask = [(ix, int(val)) for ix, val in enumerate(mask) if val != 'X']

        if 'mem' in instruc:
            # Parse Input
            instruc = instruc.split(' = ')
            pos = int(''.join(filter(str.isdigit, instruc[0])))
            num = int(instruc[1])

            # Run Mask Overwrite
            num = mask_overwrite(num, mask)
            memory_dict[pos] = num

    return sum(list(memory_dict.values()))


def revised_mask_overwrite(num, mask):
    ''' Applies the mask overwrite of part 2. Returns a list. '''
    bit = num_to_binary(num)

    # Location of 1s and Xs in the mask
    one_mask = [ix for ix,val in enumerate(mask) if val == '1']
    x_mask = [ix for ix,val in enumerate(mask) if val == 'X']

    # Location of 1s in the OG Number
    one_bit = [ix for ix,val in enumerate(bit) if val != 0 and ix not in one_mask + x_mask]

    # Get Locations of Surefire 1s then compute Base Value
    ones = one_bit + one_mask
    base_val = sum([2**(35-val) for val in ones])

    # Get All Combinations of Xs & All Resulting Possible Values
    poss_val = [2**(35-val) for val in x_mask]
    poss_comb = []

    for i in range(len(poss_val) + 1):
        poss_comb += list(combinations(poss_val, i))

    poss_val = [sum(val) + base_val for val in set(poss_comb)]

    return poss_val

def revised_initalize_program(_input):
    '''Revised initialize program code for part 2. 
    Reduced mask parsing, change to mask overwrite.'''
    memory_dict = {}

    for instruc in _input:
        if 'mask' in instruc:
            # Retrieve Mask
            mask = instruc.split(' = ')[1]

        if 'mem' in instruc:
            # Parse Input
            instruc = instruc.split(' = ')
            pos = int(''.join(filter(str.isdigit, instruc[0])))
            num = int(instruc[1])

            # Run Mask Overwrite
            pos = revised_mask_overwrite(pos, mask)
            for p in pos: memory_dict[p] = num

    return sum(list(memory_dict.values()))

if __name__ == "__main__":
    _input = open("aoc_14.txt").read().splitlines()
    
    print("PART 1")
    initalize_program(_input)
    print("")
    print("PART 2")
    revised_initalize_program(_input)
