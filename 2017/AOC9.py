def parse_excl_points(string):
    while '!' in string:
        ix = string.index('!')
        string = string[:ix] + string[ix + 2:]
    return string

def score_string(string):
    '''Scores the string. The string must have been
    parsed with parse_excl_points first.

    :param string: str being scored
    :return: int
    '''
    score, bracket_count, garbage_count = 0, 0, 0
    garbage = False

    for s in string:
        if s == '{' and not garbage:
            bracket_count += 1
        elif s == '}' and not garbage and bracket_count > 0:
            score += bracket_count
            bracket_count += -1
        elif s == '<' and not garbage:
            garbage = True
        elif s == '>' and garbage:
            garbage = False
        elif garbage:
            garbage_count += 1

    return score, garbage_count

if __name__ == '__main__':
    _input = open("2017/aoc_9.txt").read()
    _input = parse_excl_points(_input)
    sol1, sol2 = score_string(_input)  # 7616, 3838
    print(f'PART 1: {sol1} \n PART 2: {sol2}')