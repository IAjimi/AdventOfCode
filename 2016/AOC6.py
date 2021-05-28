from collections import Counter

def error_corrected_message(_input, part = 1):
    message = ''

    for i in range(len(_input[0])):
        slice = [line[i] for line in _input]
        counted_slice = Counter(slice)
        if part == 1:
            _ = max(counted_slice.values())
        else:
            _ = min(counted_slice.values())
        letter = [key for key, val in counted_slice.items() if val == _][0]
        message += letter

    return message

if __name__ == '__main__':
    _input = open("2016/aoc6.txt").read().splitlines()
    sol1 = error_corrected_message(_input, part=1)  # liwvqppc
    print(f'PART 1: {sol1}')
    sol2 = error_corrected_message(_input, part=2)  # caqfbzlh
    print(f'PART 2: {sol2}')

