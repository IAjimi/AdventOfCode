def count_at_least_one_yes(_input):
    '''Method here is to create a dictionary from the string.
    All unique letters in the string will be keys to the dict,
    so just count the number of keys. '''

    distinct_letters = dict.fromkeys(_input, 0)
    distinct_letters = len(distinct_letters.keys())

    return distinct_letters

def count_all_yes(_input):
    '''This time we need to actually count the occurences of letters
    and the number of people involved. '''

    n = _input.count('\n') + 1 # +1 bc 1st answer wont have newline
    common_letters = {letter: _input.count(letter) for letter in _input if _input.count(letter) == n}
    
    return len(common_letters.keys())

if __name__ == "__main__":
    _raw_input = open("aoc_6.txt").read()
    
    print("PART 1")
    _input = [i.replace('\n', '') for i in _raw_input.split('\n\n')]
    sum(list(map(count_at_least_one_yes, _input)))

    print("")
    print("PART 2")

    # Need to re-process input to keep \n for headcount
    _input = _raw_input.split('\n\n')
    sum(list(map(count_all_yes, _input)))