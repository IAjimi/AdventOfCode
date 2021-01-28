''' Had initially solved this just by recursively solving for 
the expressions between (). Part 2 added a twist. Initial solution I
thought of was to just find a way to add () around all sums - regex
was too involved so looked for alternate solution. Looked at 
parsing expressions, but ultimately it was just simpler to iterate
over the expressions with sums done first.'''

import functools

def parse_expression(_input):
    '''Takes math expression as a string, outputs all the numberical 
    values in expression as a list of strings and all the operators
    (parentheses included).'''
    _input = _input.split(' ')
    val = [v for ix,v in enumerate(_input) if v not in ['+', '*', ' ']]
    op = [v for ix,v in enumerate(_input) if v in ['+', '*']]
    return val, op

def find_parenthesis_block(string):
    counter = 0
    start = string.index('(')

    for ix,v in enumerate(string[start:]):
        if v == '(': 
            counter += 1
        elif v == ')': 
            counter += -1
        else:
            counter += 0
            
        if counter == 0:
            end = ix
            break
            
    return start, start + ix

def evaluate_expression(_input, add_first = False):
    '''Takes in a string without parenthesis. Computes the expression from
    left to right if add_first == False. Otherwise gives priority to 
    addition.'''
    val, op = parse_expression(_input)
    
    if add_first == False:
        # Compute from left to right
        while op:     
            result = eval(val[0] + op[0] + val[1]) 
            val = [str(result)] + val[2:]
            op.pop(0)
      
        return result

    else:
        visited = []

        # Adds everything first
        while '+' in op:
            for ix in range(len(op)):
                o = op[ix]

                if o == '+':
                    first, second = ix - len(visited), ix + 1 - len(visited)
                    result = int(val[first]) + int(val[second])
                    val = val[:first] + [result] + val[second+1:]
                    visited.append(ix)
                    print(val)

            op = [v for ix, v in enumerate(op) if ix not in visited]

        # What is left over are all numbers to be multipled together
        val = [int(v) for v in val]

        return functools.reduce(operator.mul, val) 

def do_the_math(_input, add_first = False):
    # Recursively processes () to compute the expression within
    while '(' in _input:
        temp = _input

        while '(' in temp:
            start, end = find_parenthesis_block(temp)
            temp = temp[start + 1:end]

        result = evaluate_expression(temp, add_first)
        _input = _input.replace('(' + temp + ')', str(result))  
        
    return evaluate_expression(_input, add_first) 

if __name__ == "__main__":
    _input = open("aoc_18.txt").read().splitlines()
    
    print("PART 1")
    solution = [do_the_math(_) for _ in _input]
    sum(solution) # 701339185745
    print("")
    print("PART 2")
    solution = [do_the_math(_, add_first = True) for _ in _input]
    sum(solution) # 4208490449905

