def move_forward(state, current_value, step):
    for _ in range(step):
        current_value = state[current_value]
    return current_value

def fast_spinlock(max_range, step):
    state = {0:1, 1:0}

    for _ in range(1, max_range):
        current_value = move_forward(state, _, step)

        new_val = _ + 1
        old_val = state[current_value]

        state[current_value] = new_val
        state[new_val] = old_val

        if _ % 100000 == 0: print(_, state[0])

    return state

if __name__ == "__main__":
    sol1 = fast_spinlock(max_range=2017, step=335) # 1282
    sol2 = fast_spinlock(max_range=27700000, step=335) # 27650600 - not doing full range bc too slow
    print(f'PART 1: {sol1[2017]} \n PART 2: {sol2[0]}')