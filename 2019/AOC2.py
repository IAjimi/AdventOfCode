class Intcode():
	def __init__(self, _input, noun=None, verb=None):
		self.program = [int(i) for i in _input]

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0

	def run(self):
		while self.i <= len(self.program):
			opcode = self.program[self.i]

			if opcode == 1:
				params = self.program[self.i + 1], self.program[self.i + 2], self.program[self.i + 3]
				self.program[params[2]] = self.program[params[0]] + self.program[params[1]]
				self.i += 1 + len(params)
			elif opcode == 2:
				params = self.program[self.i + 1], self.program[self.i + 2], self.program[self.i + 3]
				self.program[params[2]] = self.program[params[0]] * self.program[params[1]]
				self.i += 1 + len(params)
			elif opcode == 99:
				return self.program[0]
			else:
				raise Exception('Unknown opcode.')

if __name__ == '__main__':
	_input = open("2019/aoc2.txt").read().split(',')
	_output = Intcode(_input).run()
	print(f'PART 1: {_output}')  # 2890696

	for verb in range(0, 100):
		for noun in range(0, 100):
			_output = Intcode(_input, noun, verb).run()
			if _output == 19690720:
				print(f'PART 2: {100 * noun + verb}')  # 8226
				break
