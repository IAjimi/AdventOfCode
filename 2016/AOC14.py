import hashlib

def check_in_a_row_rep(string, x):
    if len(string) == x:
        n = 0
        for i in range(len(string)-1): # write as list comp?
            if string[i] == string[i+1]:
                n += 1
            else:
                return 0

        return 1

    else:
        return 0

def solve(salt,part=1):
    r = 0
    sol = []
    check_dict = {}

    while len(sol) < 64:
        m = hashlib.md5()
        m.update((salt + str(r)).encode('utf-8'))
        hex_m = m.hexdigest()

        if part == 2:
            for _ in range(2016):
                m = hashlib.md5()
                m.update(hex_m.encode('utf-8'))
                hex_m = m.hexdigest()

        # Check 3 peat
        rep_3_vals = [hex_m[i:i + 3] for i in range(len(hex_m))]
        rep_3_test = [check_in_a_row_rep(s, 3) for s in rep_3_vals]

        if sum(rep_3_test) >= 1:
            rep_3_ix = rep_3_test.index(1)
            rep_3_char = rep_3_vals[rep_3_ix][0]

            if rep_3_char in check_dict.keys():
                check_dict[rep_3_char].append(r)
            else:
                check_dict[rep_3_char] = [r]

            # Check 5 peat
            rep_5_vals = [hex_m[i:i + 5] for i in range(len(hex_m))]
            rep_5_test = [check_in_a_row_rep(s, 5) for s in rep_5_vals]

            if sum(rep_5_test) >= 1:
                rep_5_ix = rep_5_test.index(1)
                rep_5_char = rep_5_vals[rep_5_ix][0]

                if rep_5_char in check_dict.keys():
                    for t in check_dict[rep_5_char]:
                        if (t + 1000 >= r) and (t < r):
                            sol.append(t)

        r += 1


    return sol[64-1:]

if __name__ == '__main__':
    salt = 'yjdafjpo'

    sol1 = solve(salt)  # 25427
    print(f'PART 1: {sol1}')

    sol2 = solve(salt,part=2)
    print(f'PART 2: {sol2}')  # 22045