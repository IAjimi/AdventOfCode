class Programs:
    def __init__(self, part):
        self.registers = {letter: 0 for letter in 'abcd'}
        if part == 2:
            self.registers['c'] = 1
        self.i = 0

    def get_val(self, x):
        try:
            return int(x)
        except:
            return self.registers[x]

    def run(self, instr_list):
        while self.i < len(instr_list):
            instr = instr_list[self.i]

            if instr[:3] == 'cpy':
                self.cpy(instr[4:])
            elif instr[:3] == 'inc':
                self.inc(instr[4:])
            elif instr[:3] == 'dec':
                self.dec(instr[4:])
            elif instr[:3] == 'jnz':
                self.jnz(instr[4:])
            else:
                raise Exception('Unknown instruction.')

            if instr[:3] != 'jnz':
                self.i += 1

        return self.registers['a']

    def cpy(self, instr):
        y, x = instr.split(' ')
        y = self.get_val(y)
        self.registers[x] = y

    def inc(self, instr):
        x = instr
        self.registers[x] += 1

    def dec(self, instr):
        x = instr
        self.registers[x] += -1

    def jnz(self, instr):
        x, y = instr.split(' ')
        x = self.get_val(x)

        if x > 0:
            self.i += int(y)
        else:
            self.i += 1

if __name__ == '__main__':
    instructions = open("2016/aoc12.txt").read().splitlines()

    sol1 = Programs(part=1).run(instructions)  # 318077
    print(f'PART 1: {sol1}')

    sol2 = Programs(part=2).run(instructions)  # 9227731
    print(f'PART 2: {sol2}')