def react_polymer(string, matches):
    replacing = True

    while replacing:
        n = 0
        
        for m in matches:
            if m in string:
                n = 1
                string = string.replace(m, '')
        
        if n == 0:
            replacing = False

    return len(string)

def modify_polymer(_input, matches):
    lengths = []

    for l in ascii_lowercase:
        string = _input.replace(l, '').replace(l.title(), '')
        _len = react_polymer(string, matches)
        lengths.append(_len)

    return min(lengths)

if __name__ == "__main__":
    _input = open("aoc_5.txt").read()

    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    matches = [l + l.title() for l in ascii_lowercase]
    matches = matches + [s[::-1] for s in matches]

    print("PART 1")
    print(react_polymer(_input, matches)) # 9288
    print("PART 2")
    print(modify_polymer(_input, matches)) # 5844