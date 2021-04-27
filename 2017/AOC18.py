class Programs:
    def __init__(self, instr_list, program_id, part):
        self.instr_list = instr_list
        self.registers = {s[4]: 0 for s in self.instr_list if s in 'abcdefghijklmnopqrstuvwxyz'}  # find all programs and createvalue dict
        self.registers['p'] = program_id
        self.part = part
        self.last_played = []
        self.i = 0

    def parse_instr(self, instr):
        register, new_val = instr[4:].split(' ')
        if new_val in 'abcdefghijklmnopqrstuvwxyz':
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

    def duet(self, other_last_played = []):
        playing = True

        while playing:
            instr = self.instr_list[self.i]

            if instr[:3] == 'snd':
                register = self.process_register(instr[4])
                self.last_played.append(register)
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
                if self.part == 'pt1':
                    if (len(self.last_played) > 0) & (self.last_played[-1] > 0):
                        return self.last_played[-1]
                elif self.part == 'pt2':
                    if other_last_played:
                        register = instr[4]
                        self.registers[register] = other_last_played[0]
                        other_last_played.pop(0)
                    else:
                        return self.last_played
                else:
                    raise Exception('Unknown part.')
            elif instr[:3] == 'jgz':
                register, new_val = self.parse_instr(instr)
                register = self.process_register(instr[4])

                if register > 0:
                    self.i += new_val
                else:
                    self.i += 1
            else:
                raise Exception('Unknown instruction.')

            if instr[:3] != 'jgz':
                self.i += 1


def two_player_duet(_input):
    p0, p1 = Programs(_input, 0, 'pt2'), Programs(_input, 1, 'pt2')
    p0_last_played, p1_last_played = [], []
    p1_snd_count = 0
    deadlock = False

    while not deadlock:
        p0_last_played = p0.duet(p1_last_played)
        p1_last_played = p1.duet(p0_last_played)
        p1_snd_count += len(p1_last_played)
        if len(p1_last_played) == 0:
            return p1_snd_count

if __name__ == "__main__":
    _input = open("2017/aoc_18.txt").read().splitlines()

    sol1 = Programs(_input, 0, 'pt1').duet()  # 2951
    sol2 = two_player_duet(_input)  # 7366

    print(f"PART 1: {sol1} \n PART 2: {sol2}")
