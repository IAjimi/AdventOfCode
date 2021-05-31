import re

def aba_bab(word):
    if len(word) == 3:
        if (word[0] != word[1]) and (word[0] == word[2]):
            return word
        else:
            return ''
    else:
        return ''

def abba(word):
    if len(word) == 4:
        if (word[0] != word[1]) and (word[1] == word[2]) and (word[0] == word[3]):
            return 1
        else:
            return 0
    else:
        return 0

def find_TLS(line):
    check = 0

    for _ in range(len(line)):
        word = line[_]
        match = sum([abba(word[r:r+4]) for r in range(len(word))])
        if _ % 2 == 0:  # if even (not in bracket)
            check += match
        else:
            check += -match

    if check >= 1:
        return 1
    else:
        return 0

def find_SSL(line):
    set1, set2 = set(), set()

    for _ in range(len(line)):
        word = line[_]
        match = [aba_bab(word[r:r + 3]) for r in range(len(word))]  # 1 if aba_bab format, else ''
        match = [t for t in match if t != '']

        if _ % 2 == 0:  # if even (not in bracket)
            for t in match:
                temp = t[1] + t[0] + t[1]  # constructing match string, if aba will return bab
                set1.add(temp)
        else:
            for t in match:
                set2.add(t)

    if set1.intersection(set2) != set():
        return 1
    else:
        return 0

if __name__ == '__main__':
    _input = open("2016/aoc7.txt").read().splitlines()
    _input = [re.split(r'\[([^\]]+)\]', line) for line in _input]

    sol1 = [find_TLS(line) for line in _input]  # 110
    sol2 = [find_SSL(line) for line in _input]  # 242
    print(f'PART 1: {sum(sol1)} \n PART 2: {sum(sol2)}')
