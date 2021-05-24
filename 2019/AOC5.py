class Intcode():
	def __init__(self, program, _input, noun=None, verb=None):
		self.program = [int(i) for i in program]
		self._input = _input

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0

	def parameter_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		else:
			raise Exception('Invalid mode.')

	def get_params(self, param_mode, n_params):
		params = [None for n in range(n_params)]
		params[0] = self.parameter_mode(param_mode[0], self.program[self.i + 1])
		params[1] = self.parameter_mode(param_mode[1], self.program[self.i + 2])
		if n_params == 3:
			params[2] = self.program[self.i + 3]
		return params

	def run(self):
		while self.i <= len(self.program):
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
				params = [self.program[self.i + 1]]
				self.program[params[0]] = self._input
			elif opcode == 4:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				print(params[0])
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
			elif opcode == 99:
				return self.program[0]
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)

if __name__ == '__main__':
	_input = open("2019/aoc7.txt").read().split(',')
	Intcode(_input, 1).run()  # 16348437
	Intcode(_input, 5).run()  # 6959377