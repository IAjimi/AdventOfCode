'''Good lesson on the importance of data structures. Both parts were pretty
straightforward, but part 2 required some optimization (using a dict
of values pointing to one another instead of a shuffled list, using the -1 
method to fidn the destination cup instead of array manipulations). '''

def move_cups(_input):
    '''Naive part 1 solution.'''
    cups = [int(i) for i in _input]

    for n in range(100):
        
        # Split up cups
        current_cup = cups[0]
        move_cups = cups[1:4]
        leftover_cups = cups[4:]

        # Find Destination cup
        find_destination_cup = [l for ix,l in enumerate(leftover_cups) if l - current_cup < 0]

        if find_destination_cup:
            destination_cup = max(find_destination_cup)
        else: 
            destination_cup = max(leftover_cups)

        destination_ix = leftover_cups.index(destination_cup)

        # Move cups along
        cups = leftover_cups[:destination_ix+1] + move_cups + leftover_cups[destination_ix+1:] + [current_cup]

    # Get Final String
    ix = cups.index(1)
    string = cups[ix+1:] + cups[:ix]
    string = [str(s) for s in string]

    return ''.join(string)

def create_cups_chain(_input):
    '''Creating a linked list for part 2. '''
    cups_dict = {}
    cups = [int(i) for i in _input]
    cups = cups + [r for r in range(max(cups)+1, 1000001)]
    current_cup = cups[0]

    for n in range(len(cups)):
        if n+1 >= len(cups):
            cups_dict[cups[n]] = cups[0]
        else:
            cups_dict[cups[n]] = cups[n+1]

    del cups

    return cups_dict

def get_next_three(cups_dict, current_cup):
    first_three = []
    first_three.append(cups_dict[current_cup])
    first_three.append(cups_dict[first_three[0]])
    first_three.append(cups_dict[first_three[1]])

    return first_three

def move_alotta_cups(_input):
    cups_dict = create_cups_chain(_input)

    current_cup = int(_input[0])

    for n in range(10000000):
        # Get Next 3 Cups
        first_three = get_next_three(cups_dict, current_cup)

        # Change current_cup pointer to what is after those 3
        cups_dict[current_cup] = cups_dict[first_three[2]]

        # Look for destination_cup
        search_cup = True
        dest_val = current_cup - 1

        while search_cup:
            if dest_val in cups_dict.keys() and dest_val not in first_three:
                search_cup = False
            else:
                dest_val = dest_val - 1 if dest_val > 0 else max(cups_dict.keys())

        # Change pointers
        cups_dict[first_three[2]] = cups_dict[dest_val]
        cups_dict[dest_val] = first_three[0]

        # New current cup
        current_cup = cups_dict[current_cup]

    # Get the 2 cups clockwise of 1
    first_cup = cups_dict[1]
    second_cup = cups_dict[first_cup]

    return first_cup * second_cup
    

if __name__ == "__main__":
    _input = '538914762'
    print("PART 1")
    move_cups(_input) # 54327968
    print("")
    print("PART 2")
    move_alotta_cups(_input) # 157410423276
