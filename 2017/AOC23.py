class Programs:
    def __init__(self, instr_list):
        self.instr_list = instr_list
        self.registers = {s: 0 for s in 'abcdefgh'}  # find all programs and create value dict
        self.i = 0

    def parse_instr(self, instr):
        register, new_val = instr[4:].split(' ')
        if new_val in self.registers.keys():
            new_val = self.registers[new_val]
        else:
            new_val = int(new_val)
        return register, new_val

    def process_register(self, val):
        if val in self.registers.keys():
            val = self.registers[val]
        else:
            val = val
        return int(val)

    def duet(self):
        m = 0

        while self.i < len(self.instr_list):
            instr = self.instr_list[self.i]

            if instr[:3] == 'set':
                register, new_val = self.parse_instr(instr)
                self.registers[register] = new_val
            elif instr[:3] == 'sub':
                register, new_val = self.parse_instr(instr)
                self.registers[register] += - new_val
            elif instr[:3] == 'mul':
                register, new_val = self.parse_instr(instr)
                self.registers[register] = self.registers[register] * new_val
                m += 1
            elif instr[:3] == 'jnz':
                register, new_val = self.parse_instr(instr)
                register = self.process_register(instr[4])

                if register != 0:
                    self.i += new_val
                else:
                    self.i += 1
            else:
                raise Exception('Unknown instruction.')

            if instr[:3] != 'jnz':
                self.i += 1

        return m

def refactored_code(min_range=109900, max_range=126900):
    '''Had to read input and convert to code.

    Initially kept b,c,d,f, etc as is, with an outer while loop incrementing b by -17 while
    b != c (resetting f,d,e to 1,2,2) with two other while loops:

    >    while b != d:
    >        while b != e:
    >            if d * e - b == 0:
    >                f = 0
    >            e += 1
    >        d += 1

    The important part of this while loop is the d * e - b == 0 check: this checks to see whether b
    can be rewritten as the product of two numbers. This is equivalent to a check like p - b == b,
    where p = d * e. This allows us to 1) rewrite the two while loops as one for loop and 2) break
    the for loop when the condition is met.

    The outer while loop can be replaced by another range() function, where min_range stands for
    the initial value of b and max_range for c.
    '''
    h = 0

    for b in range(min_range, max_range+1, 17):
        f = 1

        for d in range(2, b):
            if b % d == 0:
                f = 0
                break

        if f == 0:
            h += 1

    return h

if __name__ == "__main__":
    _input = open("2017/aoc_23.txt").read().splitlines()

    sol1 = Programs(_input).duet()  # 9409
    sol2 = refactored_code()  # 913

    print(f"PART 1: {sol1} \n PART 2: {sol2}")
