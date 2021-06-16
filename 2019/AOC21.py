from collections import defaultdict

class Intcode():
	def __init__(self, program, noun=None, verb=None):
		self.program = defaultdict(int)
		for ix, val in enumerate(program):
			self.program[ix] = int(val)

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0
		self.relative_base = 0
		self._output = []
		self.done = False

	def parameter_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		elif mode == '2':
			return self.program[param + self.relative_base]
		else:
			raise Exception('Invalid mode.')

	def address_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		elif mode == '2':
			return self.program[param] + self.relative_base
		else:
			raise Exception('Invalid mode.')

	def get_params(self, param_mode, n_params):
		params = [None for n in range(n_params)]
		params[0] = self.parameter_mode(param_mode[0], self.program[self.i + 1])
		params[1] = self.parameter_mode(param_mode[1], self.program[self.i + 2])
		if n_params == 3:
			params[2] = self.address_mode(param_mode[2], self.i + 3)
		return params

	def decode_output(self):
		return ' '.join([chr(c) for c in self._output]).splitlines()

	def run(self, _input=[]):
		while self.i <= len(self.program):
			self.done = False
			instruction = self.program[self.i]
			opcode = instruction % 100
			param_mode = str(instruction // 100)
			param_mode = param_mode[::-1] + '0' * (3 - len(param_mode))
			ix_change = False

			if opcode == 1:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = params[0] + params[1]
			elif opcode == 2:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = params[0] * params[1]
			elif opcode == 3:
				if _input:
					params = [self.address_mode(param_mode[0], self.i + 1)]
					current_input = _input[0]
					_input.pop(0)
					self.program[params[0]] = current_input
				else:
					print('Input needed.')
					self.done = True
					return self
			elif opcode == 4:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self._output.append(params[0])
			elif opcode == 5:
				params = self.get_params(param_mode, 2)
				if params[0] != 0:
					self.i = params[1]
					ix_change = True
			elif opcode == 6:
				params = self.get_params(param_mode, 2)
				if params[0] == 0:
					self.i = params[1]
					ix_change = True
			elif opcode == 7:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = 1 if params[0] < params[1] else 0
			elif opcode == 8:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = 1 if params[0] == params[1] else 0
			elif opcode == 9:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self.relative_base += params[0]
			elif opcode == 99:
				self._output.append(self.program[0])
				self.done = True
				return self
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)


def translate_to_ascii(instructions):
	instructions = [ord(c) for c in instructions]
	instructions.append(10)

	return instructions

def run(_input, instructions):
	instructions = translate_to_ascii(instructions)
	computer = Intcode(_input).run(instructions)
	return computer._output[-2]

if __name__ == '__main__':
	_input = open("2019/aoc21.txt").read().rstrip().split(',')

	instructions = '''NOT C J
AND D J
NOT A T
OR T J
WALK'''
	sol1 = run(_input, instructions)  # 19359969
	print(f'PART 1: {sol1}')

	instructions = '''NOT A J
AND D J
OR T J
NOT B T
AND D T
OR T J
NOT C T
AND D T
AND H T
OR T J
RUN'''
	sol2 = run(_input, instructions)  # 1140082748
	print(f'PART 2: {sol2}')



