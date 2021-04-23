class Programs:
    def __init__(self, instr_list):
        self.instr_list = instr_list
        self.registers = {}
        self.last_played = None

    def parse_instr(self, instr):
        register, new_val = instr[4:].split(' ')
        if new_val in 'abcdefghijklmnopqrstuvwxyz':
            new_val = self.registers[new_val]
        else:
            new_val = int(new_val)
        return register, new_val

    def duet(self):
        self.registers = {s[4]:0 for s in self.instr_list} # find all programs and createvalue dict
        playing = True
        i = 0

        while playing:
            instr = self.instr_list[i]

            if instr[:3] == 'snd':
                register = self.registers[instr[4:]]
                self.last_played = register
            elif instr[:3] == 'set':
                register, new_val = self.parse_instr(instr)
                self.registers[register] = new_val
            elif instr[:3] == 'add':
                register, new_val = self.parse_instr(instr)
                self.registers[register] += new_val
            elif instr[:3] == 'mul':
                register, new_val = self.parse_instr(instr)
                self.registers[register] = self.registers[register] * new_val
            elif instr[:3] == 'mod':
                register, new_val = self.parse_instr(instr)
                self.registers[register] = self.registers[register] % new_val
            elif instr[:3] == 'rcv':
                if self.last_played > 0:
                    return self.last_played
            elif instr[:3] == 'jgz':
                register, new_val = self.parse_instr(instr)

                if self.registers[register] > 0:
                    i += new_val
                else:
                    i += 1
            else:
                raise Exception('Unknown instruction.')

            if instr[:3] != 'jgz':
                i += 1




if __name__ == "__main__":
    _input = open("2017/aoc_18.txt").read().splitlines()

    sol1 = Programs(_input).duet() # 2951
    sol2 = 'idk'

    print(f"PART 1: {sol1} \n PART 2: {sol2}")