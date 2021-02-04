''' Method could be more elegant instead of iterating over dict over and over again.
Some issues with the naive regex used initially (partial matches leading to replacement).
Runs pretty quick for part 1 (<1 sec).'''

import re

def parse_input(_input):
    _input = _input.split('\n\n')
    rules = _input[0].splitlines()
    messages = _input[1].splitlines()
    return rules, messages

def parse_rules(string):
    if '"' in string:
        return string.replace('"', '')
    else:
        _list = string.split(' | ')
        return _list

def generate_matches(rules):
    '''Takes input and parses it. Finds the end keys (rules that directly map
    to a character) and iteratively replace references to those rules with
    those characters. The final element of the graph dict contains the final 
    regex.'''

    graph = {t.split(': ')[0]:parse_rules(t.split(': ')[1]) for t in rules}

    unfinished_keys, end_keys = [1], []
    
    while len(unfinished_keys) > 0:
        # Update String / Graph Dicts
        end_keys = end_keys + [k for k, v in graph.items() if type(v) == str] #keys that were turned to regex
        string_dict = {k:v for k, v in graph.items() if k in end_keys} # dict of regex
        unfinished_keys = [k for k in graph.keys() if k not in end_keys] # keys that aren't regex yet

        for key in unfinished_keys:
            val = graph[key]
            
            # Replace References to Rules w/ Proper Characters
            for k, v in string_dict.items():
                val = [re.sub('^' + k + '$', v, s) for s in val] # direct match to character
                val = [re.sub('^' + k + ' ', v + ' ', s) for s in val] # 1st element of string
                val = [re.sub(' ' + k + '$', ' ' + v, s) for s in val] # 2nd element of string
                val = [re.sub(' ' + k + ' ', ' ' + v + ' ', s) for s in val] # mid element of string

            # Count Numbers
            num = [c.isdigit() for s in val for c in s ]

            # If turned into string, Generate Regex
            if sum(num) == 0:
                val = [s.replace(' ', '') for s in val]
                graph[key] = '(' + '|'.join(val) + ')'
            # Else, update value in dict
            else:
                graph[key] = val               

    return graph['0']

def count_matches(strings, regex):
    matches = [bool(re.match(regex, s)) for s in strings]
    return sum(matches)


if __name__ == "__main__":
    _input = open("aoc_19.txt").read()
    
    print("PART 1")
    rules, messages = parse_input(_input)
    regex = generate_matches(rules)
    real_regex = '^' + regex + '$' # Exact match only
    count_matches(messages, real_regex) # 208
    print("")
    print("PART 2")


