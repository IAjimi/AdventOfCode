def process_instructions(pin_pad, line, x, y):
    for i in line:
        if i == 'U':
            if (x, y - 1) in pin_pad.keys():
                y += - 1
        elif i == 'D':
            if (x, y + 1) in pin_pad.keys():
                y += 1
        elif i == 'L':
            if (x - 1, y) in pin_pad.keys():
                x += - 1
        elif i == 'R':
            if (x + 1, y) in pin_pad.keys():
                x += 1
        else:
            raise Exception('Invalid instruction.')

    return x, y

def find_code(instructions, part):
    if part == 1:
        pin_pad = '''1 2 3
4 5 6
7 8 9'''.splitlines()
        pin_pad = [line.split(' ') for line in pin_pad]
        pin_pad = {(j, i): pin_pad[i][j] for j in range(3) for i in range(3)}
    else:
        pin_pad = {
            (0, -2): '1',
            (-1, -1): '2',
            (0, -1): '3',
            (1, -1): '4',
            (-2, 0): '5',
            (-1, 0): '6',
            (0, 0): '7',
            (1, 0): '8',
            (2, 0): '9',
            (-1, 1): 'A',
            (0, 1): 'B',
            (1, 1): 'C',
            (0, 2): 'D'
        }

    code = []
    if part == 1:
        x, y = 1, 1
    else:
        x, y = -2, 0

    for line in instructions:
        x, y = process_instructions(pin_pad, line, x, y)
        code.append(pin_pad[(x,y)])

    return ''.join(code)

if __name__ == '__main__':
    instructions = open("2016/aoc2.txt").read().splitlines()

    sol1 = find_code(instructions, part=1)  # 92435
    print(f'PART 1: {sol1}')
    sol2 = find_code(instructions, part=2)  # C1A88
    print(f'PART 2: {sol2}')