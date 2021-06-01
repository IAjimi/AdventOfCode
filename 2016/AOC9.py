def process_line(line, part):
    '''Returns the final length of the line after processing the expression.

    :param line: str
    :param part: int, 1 for part 1 solution, 2 for part 2 solution
    :return: int
    '''
    i = 0
    sol = 0
    while line != '':
        if '(' in line: # () expression to evaluate
            pos1 = line.index('(')
            pos2 = line.index(')')
            nchar, nrep = list(map(int, line[pos1 + 1:pos2].split('x')))

            if part == 1:  # just add length of string ahead without account for () within
                new_sol = nchar
            else:  # recursively process all () within the expression
                new_sol = process_line(line[pos2 + 1:pos2 + 1 + nchar], part=part)

            sol += pos1 + (nrep * new_sol)  # add everything up to ( + the expression repeated by ()

            line = line[pos2 + 1 + nchar:]  # move along the line
        else:  # no (, add what's length of line and terminate expression
            sol += len(line)
            line = ''

    return sol

if __name__ == '__main__':
    _input = open("2016/aoc9.txt").read().splitlines()

    sol1 = [process_line(line, part=1) for line in _input]  # 152851
    sol2 = [process_line(line, part=2) for line in _input]  # 11797310782
    print(f'PART 1: {sol1[0]} \n PART 2: {sol2[0]}')