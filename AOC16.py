''' Logic-wise fairly straightforward but couldn't find an elegant way to execute the code.'''

import re
import functools, operator

def ticket_scanning_error_rate(_input):
    ''' The 1st part of the answer just ignores the fact that fields
    and tickets are meant to be separate things. Instead, a list of valid
    value ranges is made using part 1 of the input. Values that don't match
    are stored as invalid, with no distinction by ticket since all we need
    is the sum of invalid values.'''

    # Getting Acceptable Values
    num = re.sub('([a-zA-Z]+)|(:)|(\n)', '', _input[0])
    num = [n.split('-') for n in num.split(' ') if n != '']
    num = [r for n in num for r in range(int(n[0]),int(n[1]) + 1)]
    acceptable_values = set(num)

    # Getting Ticket Values
    tickets = [t for t in _input[-1].replace('nearby tickets:\n', '').split('\n')]
    tickets = [int(t) for t in ','.join(tickets).split(',')]

    # Returning Invalid Ticket Values
    invalid_vals = [t for t in tickets if t not in acceptable_values]
    
    return sum(invalid_vals)

def parse_num(string):
    string = string.split(' or ')
    string = [list(map(int, s.split('-'))) for s in string]
    string = [r for s in string for r in range(s[0], s[1] + 1)]
    return string

def parsing_input(_input):
    ''' Takes input and returns values that can be used with other functions.

    PARAMETERS:
    _input: String with very specific format.

    RETURNS:
    field_names: List of field names.
        -> EX: ['class', 'row', 'seat']
    num: List of the list of valid numbers for every field, e.g., [[field_1], [field_2], [field_2]].
        -> EX: [[0, 1, ..., 19],
                [0, 1, ..., 19],
                [0, 1, ..., 19]]
    valid_tickets: List of list of values (the list of values mapping to 1 ticket), 
    e.g., [[ticket_1], [ticket_2], [ticket_3], [ticket_4]].
        -> EX: [[3, 9, 18], [15, 1, 5], [5, 14, 9], [11, 12, 13]]
    your_ticket: List of values for your ticket.
        -> EX: [11, 12, 13]
    acceptable_values: Set of the union of valid numbers for every field.
        -> EX: {0, 1, ..., 19}
    '''

    # Get Field Names
    field_names = [t.split(': ')[0] for t in _input[0].split('\n')]

    # Get Range of Values for Every Field
    all_field_names = '|'.join(field_names)
    num = re.sub(all_field_names + '|: ', '', _input[0])
    num = num.split('\n')
    num = [parse_num(n) for n in num]

    # Get Acceptable Values
    acceptable_values = set([i for n in num for i in n])

    # Get Your Ticket
    your_ticket = _input[1].replace('your ticket:\n', '').split(',')
    your_ticket = [int(t) for t in your_ticket]

    # Parse Tickets, where 1 Ticket = 1 Sub-List 
    tickets = [t.split(',') for t in _input[-1].replace('nearby tickets:\n', '').split('\n')]
    tickets = [list(map(int, t)) for t in tickets]
    tickets = tickets + [your_ticket]

    # Only Keep Valid Tickets
    valid_tickets = [t for t in tickets if set(t).difference(acceptable_values) == set()]

    return field_names, num, valid_tickets, your_ticket, acceptable_values


def identify_impossible_positions(rules_dict, pos_dict):
    '''Takes a dict of values that don't match with each key and a dict of values
    per position. Uses both to find which fields are incompatible with certain positions.
    Returns a dict of possible positions per field.

    PARAMETERS:
    rules_dict = {field_a: {values that don't match with field_a}}
        -> EX. {'class': {2,3}, 'row': {6,7}, 'seat': {14,15}}
    pos_dict = {position_0: [ticket values in position 0]}
        -> EX. {0: [11, 3, 15, 5], 1: [12, 9, 1, 14], 2: [13, 18, 5, 9]}

    RETURNS:
    elimination_dict = {'field_a': [positions field_a could be in]} 
        -> EX. {'class': [1, 2], 'row': [0, 1, 2], 'seat': [2]}
    '''
    elimination_dict = {k:[r for r in range(len(field_names))] for k in field_names}

    for key in rules_dict.keys():
        for pos in pos_dict.keys():
            inter_ = rules_dict[key].intersection(pos_dict[pos])
            
            if inter_: 
                elimination_dict[key].remove(pos)

    return elimination_dict


def process_of_elimination(elimination_dict):
    '''Takes dict and goes through an iterative elimination process.
    When a field only has 1 possible position left, the field is added to
    correct_mapping and that position is removed from the possible positions
    of all other fields. This continues until elimination_dict is empty, i.e.,
    all fields have been matched.

    PARAMETERS:
    elimination_dict = {'field_a': [positions field_a could be in]}
        -> EX. {'class': [1, 2], 'row': [0, 1, 2], 'seat': [2]}

    RETURNS:
    correct_mapping = {'field_a': [position field a is in]}
        -> EX. {'class': 1, 'row': 0, 'seat': 2}
    '''
    correct_mapping = {}

    while elimination_dict:
        initial_key = [k for k,v in elimination_dict.items() if len(v) == 1]
        key = initial_key[0]
        
        correct_pos = elimination_dict[key][0]
        correct_mapping[key] = correct_pos
        del elimination_dict[key]

        for other_key in elimination_dict:
            elimination_dict[other_key].remove(correct_pos)

    return correct_mapping

def find_field_positons(field_names, num, valid_tickets, your_ticket, acceptable_values):
    ''' 
    Conceptually, use field_name and num to create dict with valid values for every field.
    Then use acceptable_values to find values that are INVALID for every field.
    
    Rotate all tickets to have a dictionary of ticket values for every position.

    identify_impossible_positions finds positions that a field can't be in.
    process_of_elimination then iterates over the positions to match all fields to 
    the correct position.

    The position of the fields is then used to return the final product.

    PARAMETERS:
    field_names: List of field names.
    num: List of the list of valid numbers for every field.
    valid_tickets: List of list of values (the list of values mapping to 1 ticket).
    your_ticket: List of values.
    acceptable_values: Set of the union of valid numbers for every field.

    RETURNS:
    The product of values with 'departure' in the field name of your ticket.'''

    # Create Rules Dict, Find Missing Values for Each Field
    rules_dict = {field_names[n]:num[n] for n in range(len(field_names))}

    for key in rules_dict.keys():
        rules_dict[key] = acceptable_values.difference(rules_dict[key])

    # Create Dictionary with Positions in Ticket for nth Field
    ## 0: [all position 0 values for valid tickets]
    pos_dict = {n:[v[n] for v in valid_tickets] for n in range(len(valid_tickets[0]))}

    # Ientify discrepancies between field possible values and tickets per position
    elimination_dict = identify_impossible_positions(rules_dict, pos_dict)

    # Takes dict with possible position per field and goes through elimination process 
    correct_mapping = process_of_elimination(elimination_dict)

    # Get Departure Field Value
    departure_field_pos = [v for k,v in correct_mapping.items() if 'departure' in k]
    your_ticket_departures = [v for ix,v in enumerate(your_ticket) if ix in departure_fields]

    return functools.reduce(operator.mul, your_ticket_departures)    

if __name__ == "__main__":
    _input = open("aoc_16.txt").read().split('\n\n')
    
    print("PART 1")
    ticket_scanning_error_rate(_input)
    print("")
    print("PART 2")
    field_names, num, valid_tickets, your_ticket, acceptable_values = parsing_input(_input)
    find_field_positons(field_names, num, valid_tickets, your_ticket, acceptable_values)

