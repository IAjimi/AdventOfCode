from collections import Counter

def check_validity_pt1(passphrase):
    '''Takes list of words, returns validity of list.'''
    _count = set(Counter(passphrase).values())

    if _count.difference({1}): # there are elements in _count that are > 1
        return 0
    else:
        return 1

def check_validity_pt2(passphrase):
    ## check _input[1]
    words = [Counter(p) for p in passphrase]

    for ix,word in enumerate(words):
        other_words = [1 for i, w in enumerate(words) if i != ix and w == word]

        if other_words:
            return 0
    return 1


if __name__ == "__main__":
    _input = open("2017/aoc_4.txt").read().splitlines()
    _input = [i.split() for i in _input]

    sol1 = sum(map(check_validity_pt1, _input)) # 477
    sol2 = sum(map(check_validity_pt2, _input))  # 167
    print(f"PART 1: {sol1} \n PART 2: {sol2}")