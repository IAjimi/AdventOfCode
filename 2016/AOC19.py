def move_by(_input, current, r):
    for _ in range(r):
        _next = _input[current]

        _prev = current
        current = _next

    return _prev, current

def present_game(max_range, part):
    i = 0
    current = 1

    _input = {v:v+1 for v in range(1, max_range+1)}
    _input[max_range] = 1

    while _input:
        i += 1

        if i % 150 == 0: print(i, current)

        if part == 1:
            _prev, _next = move_by(_input, current, 2)
            _input[current] = _next
            del _input[_prev]
        else:
            # Removing the elf across the circle is same as removing pos that is floor(length / 2) away
            move = round(len(_input) / 2 - 0.00001)
            _prev, _remove = move_by(_input, current, move)

            _input[_prev] = _input[_remove]  # update position of node that led to elf being removed
            del _input[_remove]  # remove elf

            _next = _input[current]  # move current elf by 1

        # Update position or end loop
        if current != _next:
            current = _next
        else:
            return current

if __name__ == '__main__':
    sol1 = present_game(3017957, part=1)  # 1841611
    print(f'PART 1: {sol1}')

    #sol2 = present_game(3017957, part=2)
    #print(f'PART 2: {sol2}')
