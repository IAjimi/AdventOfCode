def get_location(instruction):
    instruction = instruction.split(': ')
    left, top = [int(t) for t in instruction[0].split(',')]
    width, height = [int(t) for t in instruction[1].split('x')]

    output = [(left + l, top + r) for l in range(width) for r in range(height)]

    return output

def find_claims(_input):
    claims = {}
    _ids = [t.split('@ ')[0].replace('#', '') for t in _input]
    _input = [t.split('@ ')[1] for t in _input]

    for i in range(len(_input)):
        _id = int(_ids[i])
        locations = get_location(_input[i])
        
        for l in locations:
            if l in claims.keys():
                claims[l].append(_id)
            else:
                claims[l] = [_id]

    return claims

if __name__ == "__main__":
    _input = open("2018/aoc_3.txt").read().splitlines()
    claims = find_claims(_input)

    print("PART 1")
    multiple_claims = [1 for k,v in claims.items() if len(v) > 1]
    print(sum(multiple_claims))  # 107043
    print("PART 2")
    claim_ids = [v for k,v in claims.items() if len(v) > 1]
    invalid_ids = set([item for sublist in claim_ids for item in sublist])
    relevant_id = [r for r in range(1,len(_input)) if r not in invalid_ids][0]
    print(relevant_id)  # 346