def decimalToBinary(n):
    return bin(n).replace("0b", "")

def run_generators_pt1(genA, genB):
    n = 0

    for _ in range(40000000):
        genA = (16807 * genA) % 2147483647
        genB = (48271 * genB) % 2147483647
        binA = decimalToBinary(genA)
        binB = decimalToBinary(genB)

        if binA[-16:] == binB[-16:]:
            n += 1
            if n % 30 == 0: print(_, n)

    return n

def run_generators_pt2(genA, genB):
    n = 0

    for _ in range(5000000):
        genA = (16807 * genA) % 2147483647
        genB = (48271 * genB) % 2147483647

        while genA % 4 != 0:
            genA = (16807 * genA) % 2147483647

        while genB % 8 != 0:
            genB = (48271 * genB) % 2147483647

        binA = decimalToBinary(genA)
        binB = decimalToBinary(genB)

        if binA[-16:] == binB[-16:]:
            n += 1
            if n % 30 == 0: print(_, n)

    return n

if __name__ == "__main__":
    sol1 = run_generators_pt1(634, 301) # 573
    sol2 = run_generators_pt2(634, 301) # 294
    print(f"PART 1: {sol1} \n PART 2: {sol2}")