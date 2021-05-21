from collections import Counter

def parse_line(line):
    hotel, checksum = line.split('[')
    checksum = checksum[:-1]

    hotel_id = int(hotel[-3:])
    hotel_name = hotel[:-3].replace('-', '')
    return hotel_name, checksum, hotel_id

def check_hotel_name(hotel_name, checksum):
    # Get count of letters in hotel name
    hotel_count = Counter(hotel_name)
    hotel_count = sorted(hotel_count.items(), key=lambda x: x[1], reverse=True)

    # Get top 5 by count, w/ alphabetical order breaking ties
    vals = list(set([h[1] for h in hotel_count[:5]])) # gets unique values of count in top 5, e.g., [1,2,3]
    vals.sort(reverse=True) # sorts in reverse order, e.g., [3,2,1]

    sol1 = []
    for v in vals:
        temp = [h[0] for h in hotel_count if h[1] == v] # get all values w/ count == v
        temp.sort() # sort by alphabetical order
        sol1.extend(temp) # add to sol1

    sol1 = ''.join(sol1[:5])

    if sol1 == checksum:
        return 1
    else:
        return 0

def decrypt_hotel_name(hotel_name, hotel_id):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    encrypt_key = {letters[i]:letters[(i + hotel_id) % 26] for i in range(len(letters))}

    decrypted_name = ''.join([encrypt_key[t] if t != '-' else ' ' for t in hotel_name])
    return decrypted_name, hotel_id

if __name__ == '__main__':
    _input = open("2016/aoc4.txt").read().splitlines()
    _input = [parse_line(line) for line in _input]

    sol1 = sum([line[2] for line in _input if check_hotel_name(line[0], line[1]) == 1])
    print(f'PART 1: {sol1}')  # 158835

    for line in _input:
        temp = decrypt_hotel_name(line[0], line[2])
        if 'northpole' in temp[0]:
            sol2 = temp

    print(f'PART 2: {sol2}')  # ('northpoleobjectstorage', 993)




