def turing_machine():
    ix = 0
    state = 'A'
    tape = {}

    for r in range(12656374+1):
        if r % 1000000 == 0:
            print(r, sum(tape.values()))
        if state == 'A':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 0, -1, 'C'
            else:
                new_val, delta_ix, new_state = 1, 1, 'B'
        elif state == 'B':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 1, -1, 'D'
            else:
                new_val, delta_ix, new_state = 1, -1, 'A'
        elif state == 'C':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 0, 1, 'C'
            else:
                new_val, delta_ix, new_state = 1, 1, 'D'
        elif state == 'D':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 0, 1, 'E'
            else:
                new_val, delta_ix, new_state = 0, -1, 'B'
        elif state == 'E':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 1, -1, 'F'
            else:
                new_val, delta_ix, new_state = 1, 1, 'C'
        elif state == 'F':
            if (ix in tape.keys()) and (tape[ix] == 1):
                new_val, delta_ix, new_state = 1, 1, 'A'
            else:
                new_val, delta_ix, new_state = 1, -1, 'E'
        else:
            raise Exception('Unknown state.')

        tape[ix] = new_val
        ix += delta_ix
        state = new_state

    return sum(tape.values())

if __name__ == "__main__":
    sol1 = turing_machine()  # 2526
    sol2 = 'not enough stars'

    print(f"PART 1: {sol1} \n PART 2: {sol2}")
