class Programs:
    def __init__(self, n = 5):
        self.s = [i for i in 'abcdefghijklmnopqrst'[:n]]

    def dance(self, instr_list):
        for instr in instr_list:
            self.run_instruction(instr)
        return ''.join(self.s)

    def run_instruction(self, instr):
        if instr[0] == 's':
            self.spin(instr[1:])
        elif instr[0] == 'x':
            self.exchange(instr[1:])
        elif instr[0] == 'p':
            self.partner(instr[1:])
        else:
            raise Exception('Unknown instruction.')

    def spin(self, instr):
        X = int(instr)
        self.s = self.s[-X:] + self.s[:-X]

    def exchange(self, instr):
        A, B = instr.split('/')
        A, B = int(A), int(B)
        self.s[A], self.s[B] = self.s[B], self.s[A]

    def partner(self, instr):
        A, B = instr.split('/')
        A, B = self.s.index(A), self.s.index(B)
        self.s[A], self.s[B] = self.s[B], self.s[A]

def find_cycle(_input, sol1):
    sols = []
    dance = Programs(16)
    for _ in range(150):
        latest_d = dance.dance(_input)
        if latest_d == sol1 and sols.count(sol1) == 1:
            cycle = _ # 56
        sols.append(latest_d)

    sol2 = sols[1000000000 % cycle - 1]
    return sol2

if __name__ == "__main__":
    _input = open("2017/aoc_16.txt").read().split(',')

    sol1 = Programs(16).dance(_input) # lbdiomkhgcjanefp
    sol2 = find_cycle(_input, sol1) # ejkflpgnamhdcboi

    print(f"PART 1: {sol1} \n PART 2: {sol2}")