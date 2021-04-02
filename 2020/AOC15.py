def memory_game(_input, turns):
    ''' Takes a couple of seconds to run for part 2.

    Initial execution was a bit cleaner code-wise
    but relied on storing everything in an increasingly long
    array. This version uses a dict to store the 2 latest times
    the number appears, which is more efficient memory-wise.'''
    sequence = {val:[ix+1] for ix, val in enumerate(_input)}
    n = len(_input)
    last_num = _input[-1]

    while n <= turns:
        if last_num not in sequence.keys():
            sequence[last_num] = [n]

        # Update Spoken Times
        spoken_times = sequence[last_num]
        spoken_times = [spoken_times[-1]] + [n]
        sequence[last_num] = spoken_times

        # Get # of Turns since Last Spoken
        if len(spoken_times) > 1:
            last_num = spoken_times[1] - spoken_times[0]
        else:
            last_num = 0

        n += 1

        # Keep Track of Exec when Slow
        if n % 2500000 == 0: print(n) 

    return {k for k,v in sequence.items() if turns in v}

if __name__ == "__main__":
    _input = [2,15,0,9,1,20]
    
    print("PART 1")
    memory_game(_input, 2020)
    print("")
    print("PART 2")
    memory_game(_input, 30000000)