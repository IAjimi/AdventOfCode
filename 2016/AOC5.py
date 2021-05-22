import hashlib

def crack_password(door_id, part):
    i = 0
    ix = 0
    password = ['_' for _ in range(8)]

    while len([p for p in password if p != '_']) < 8:
        i += 1

        m = hashlib.md5()
        m.update((door_id + str(i)).encode('utf-8'))
        hex_m = m.hexdigest()

        if hex_m[:5] == '00000':
            if part == 1:
                val = hex_m[5]
                password[ix] = val
                ix += 1
                print(ix, val)
            else:
                try:
                    ix = int(hex_m[5])
                    val = hex_m[6]
                    if ix < len(password) and password[ix] == '_':
                        password[ix] = val
                        print(''.join(password))
                except:
                    ix = 0

    return ''.join(password)

if __name__ == '__main__':
    sol1 = crack_password('wtnhxymk', 1)  # 2414bc77
    print(f'PART 1: {sol1}')
    sol2 = crack_password('wtnhxymk', 2)  # 437e60fc
    print(f'PART 2: {sol2}')