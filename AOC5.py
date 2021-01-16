def find_seat(_input, range_length):
    '''This solves the problem using a 'distance travelled' approach
    to the problem. 

    We move the midpoint of every interval either towards 0 (-) or
    the end of the range (+) based on the letter. The distance travelled
    does not depend on the letter and is always an exponent of 2, since this
    distanced is halved every turn.

    We start at the midpoint of the range (start). Our initial distance 
    travelled is f (we start at half of the range, so 1st move is 1/2 that).

    The end position is our starting position + the distance travelled.
    '''

    start = ((range_length - 1) / 2)
    f = range_length / 4

    signs = [1 if l in ["B", "R"] else -1 for l in _input]
    weights = [f *(2**-i) for i, e in enumerate(signs)]

    signs, weights = np.array(signs), np.array(weights)

    vals = signs * weights

    return start + sum(vals)

def compute_seat_id(_input, row_length, col_length):
    # Split String
    row_instruc, col_instruc = _input[:-3], _input[-3:]

    # Get Seat Number
    row_val = find_seat(row_instruc, row_length)
    col_val = find_seat(col_instruc, col_length)

    return (row_val * 8) + col_val

def elimination_process(_input):
    # Find & Remove Seats w/ Neighbors
    drop_seats = [s for s in all_seat_ids if s + 1 in all_seat_ids and s - 1 in all_seat_ids]

    # Rest is Solution Candidates
    neighbor_candidates = [s for s in all_seat_ids if s not in drop_seats]

    # Actual Solution Seats will have another candidate seat 2 places away in either direction
    solution = [s for s in neighbor_candidates if s + 2 in neighbor_candidates or s - 2 in neighbor_candidates]

    return np.mean(solution)

if __name__ == "__main__":
    import numpy as np

    _input = open("aoc_5.txt").read().splitlines()
    
    print("PART 1")
    all_seat_ids = list(map(compute_seat_id, _input, [128 for i in _input], [8 for i in _input]))
    max(all_seat_ids)
    print("")
    print("PART 2")
    elimination_process(all_seat_ids)