import copy

def find_neighbors(_input, i, j):
    ''' Very similar to the functions used to find seats in line of sight for part 2,
    except this only allows for 1 iteration of the find_first_seen process.'''
    n = len(_input)
    m = len(_input[0])
    neighbors = []
    possible_angles = [(-1, 0), (-1,-1), (-1, 1), (1, 0), (1,-1), (1,1), (0,-1), (0,1)]
    
    for x,y in possible_angles:
        k = i + x
        l = j + y
        
        if (k >= 0) and (k <= n - 1) and (l >= 0) and (l <= m - 1):
            if _input[k][l] != '.': neighbors.append( (k,l) )

    return neighbors

def find_first_seen(_input, i, j, x, y):
    ''' Increases i and j by x and y respectively until either
    the new point is outside the seating chart or a seat (not '.')
    is found.'''

    found = False
    n = len(_input)
    m = len(_input[0])

    while found == False:
        i += x
        j += y
        
        if (i < 0) or (i >= n) or (j < 0) or (j >= m):
            break
        else:
            if _input[i][j] != '.':
                return i,j

def find_line_of_view_neighbors(_input, i, j):
    n = len(_input)
    m = len(_input[0])
    neighbors = []
    possible_angles = [(-1, 0), (-1,-1), (-1, 1), (1, 0), (1,-1), (1,1), (0,-1), (0,1)]

    for x,y in possible_angles:
        neigh = find_first_seen(_input, i, j, x, y)
        if neigh: neighbors.append(neigh)

    return neighbors

def wait_for_convergence(_input, seats, neighbor_dict, switch):
    is_changing = True

    while is_changing == True:
        n = 0
        temp_map = copy.deepcopy(_input)
        
        for i,j in seats:
            seat_val = _input[i][j]
            neighbors = neighbor_dict[(i,j)]
            occupied_neighbors = [_input[i][j] for i,j in neighbors]
            occupied_neighbors = sum([1 if neigh == '#' else 0 for neigh in occupied_neighbors])

            if seat_val == 'L' and occupied_neighbors == 0:
                temp_map[i] = temp_map[i][:j] + '#' + temp_map[i][j+1:]
                n += 1
            elif seat_val == '#' and occupied_neighbors >= switch:
                temp_map[i] = temp_map[i][:j] + 'L' + temp_map[i][j+1:]
                n += 1

        _input = temp_map
                
        # If no more change in seats
        if n == 0:
            flattened_input = ''.join(_input)
            final_occupied_seats = sum([1 if seat == '#' else 0 for seat in flattened_input])
            return final_occupied_seats

if __name__ == "__main__":
    _input = open("aoc_11.txt").read().splitlines()
    seats = [(i,j) for i,row in enumerate(_input) for j,col in enumerate(row) if col != '.']
    
    print("PART 1")
    neighbor_dict = {(i,j):find_neighbors(_input, i, j) for i,j in seats}
    n = wait_for_convergence(_input, seats, neighbor_dict, 4)
    print(n)
    print("")
    print("PART 2")
    neighbor_dict = {(i,j):find_line_of_view_neighbors(_input, i, j) for i,j in seats}
    n = wait_for_convergence(_input, seats, neighbor_dict, 5)
    print(n)

