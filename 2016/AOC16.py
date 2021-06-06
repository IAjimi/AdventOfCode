def solve(initial_state, max_n):
    current = initial_state

    while len(current) < max_n:
        new = current[::-1]
        new = ''.join(['1' if c == '0' else '0' for c in new])
        current += '0' + new

    current = current[:max_n]

    while len(current) % 2 == 0:
        checksum = [current[r:r+2] for r in range(0, len(current), 2)]
        checksum = ['1' if c in ['11', '00'] else '0' for c in checksum]
        current = ''.join(checksum)

    return current

if __name__ == '__main__':
    initial_state = '11110010111001001'

    sol1 = solve(initial_state, 272)  # 01110011101111011
    print(f'PART 1: {sol1}')
    sol2 = solve(initial_state, 35651584)  # 11001111011000111
    print(f'PART 2: {sol2}')